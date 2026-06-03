#!/usr/bin/env python3
"""
generate_openapi.py — Genera un spec OpenAPI 3.0 analizando un backend Express.
Generates an OpenAPI 3.0 spec by statically analyzing an Express backend.

Estrategia (fallback b): cuando el backend NO expone Swagger, se analiza el
archivo de arranque (app.ts/app.js) para descubrir los `app.use("/prefix", router)`
y luego cada archivo *.router.* para extraer endpoints
`Router.get/post/put/delete/patch("/path", ...handlers, Controller.method)`.

Solo stdlib. / Stdlib only.

Uso / Usage:
    python3 generate_openapi.py <repo_path> [--entry src/app.ts] [--out openapi.json] [--title "API"]
"""
import json
import os
import re
import sys


HTTP_METHODS = ("get", "post", "put", "delete", "patch", "options", "head")


def find_entry(repo):
    for cand in ("src/app.ts", "src/app.js", "src/server.ts", "src/server.js",
                 "src/index.ts", "src/index.js", "app.ts", "app.js", "index.ts", "index.js"):
        p = os.path.join(repo, cand)
        if os.path.isfile(p):
            return p
    return None


def parse_imports(text):
    """Mapa nombreVariable -> ruta relativa de import (sin extensión)."""
    imports = {}
    # import X from '...'
    for m in re.finditer(r"import\s+([A-Za-z0-9_]+)\s+from\s+['\"]([^'\"]+)['\"]", text):
        imports[m.group(1)] = m.group(2)
    # import { X } from '...'  (toma cada nombre)
    for m in re.finditer(r"import\s*\{([^}]+)\}\s*from\s*['\"]([^'\"]+)['\"]", text):
        for name in m.group(1).split(","):
            name = name.strip().split(" as ")[-1].strip()
            if name:
                imports[name] = m.group(2)
    return imports


def resolve_import(repo, entry_dir, rel):
    """Resuelve una ruta de import a un archivo real."""
    if not rel.startswith("."):
        # alias tipo 'src/...' o '@middlewares/...': intentar desde la raíz
        base = os.path.join(repo, rel.lstrip("@").replace("middlewares", "src/middlewares"))
        candidates = [base]
    else:
        candidates = [os.path.normpath(os.path.join(entry_dir, rel))]
    exts = ["", ".ts", ".js", "/index.ts", "/index.js"]
    for c in candidates:
        for e in exts:
            p = c + e
            if os.path.isfile(p):
                return p
    return None


def find_mounts(text):
    """Lista de (prefix, routerVar) desde app.use("/prefix", routerVar)."""
    mounts = []
    for m in re.finditer(r"""app\.use\(\s*['"]([^'"]+)['"]\s*,\s*([A-Za-z0-9_]+)\s*\)""", text):
        prefix = m.group(1)
        var = m.group(2)
        # Ignorar middlewares globales tipo cors()/express.json()
        mounts.append((prefix, var))
    return mounts


def parse_router_file(path):
    """Extrae endpoints de un archivo router de Express."""
    endpoints = []
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    except Exception:
        return endpoints
    # Captura: <algo>.<method>( '<path>' , ... <Controller.method> )
    pattern = re.compile(
        r"""([A-Za-z0-9_]+)\.(%s)\(\s*['"]([^'"]+)['"]([^;]*?)\)""" % "|".join(HTTP_METHODS),
        re.DOTALL,
    )
    for m in pattern.finditer(text):
        method = m.group(2).upper()
        route = m.group(3)
        tail = m.group(4)
        # handler = último identificador Controller.metodo o func
        handlers = re.findall(r"([A-Za-z0-9_]+\.[A-Za-z0-9_]+)", tail)
        handler = handlers[-1] if handlers else None
        # detectar middlewares de auth/validación por nombre
        secured = bool(re.search(r"validateToken|verifyToken|auth|Auth", tail))
        endpoints.append({
            "method": method,
            "route": route,
            "handler": handler,
            "secured": secured,
        })
    return endpoints


def clean_prefix(prefix):
    # quita comodines tipo /banking/v1/* -> /banking/v1
    return re.sub(r"/\*+$", "", prefix)


def join_path(prefix, route):
    p = clean_prefix(prefix).rstrip("/")
    r = route if route.startswith("/") else "/" + route
    full = (p + r) if r != "/" else (p or "/")
    return re.sub(r"/{2,}", "/", full) or "/"


def to_openapi(repo, entry, title, version):
    entry_dir = os.path.dirname(entry)
    with open(entry, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    imports = parse_imports(text)
    mounts = find_mounts(text)

    paths = {}
    tags = {}
    total = 0
    for prefix, var in mounts:
        rel = imports.get(var)
        if not rel:
            continue
        router_file = resolve_import(repo, entry_dir, rel)
        if not router_file or not re.search(r"router", os.path.basename(router_file), re.I):
            # solo procesar si parece router
            if not router_file or ".router" not in os.path.basename(router_file).lower():
                continue
        tag = clean_prefix(prefix).strip("/").split("/")[0] or "root"
        tags.setdefault(tag, prefix)
        for ep in parse_router_file(router_file):
            full = join_path(prefix, ep["route"])
            item = paths.setdefault(full, {})
            op = {
                "tags": [tag],
                "summary": ep["handler"] or "endpoint",
                "operationId": (ep["handler"] or "op").replace(".", "_") + "_" + ep["method"].lower(),
                "responses": {"200": {"description": "OK"}},
            }
            if ep["secured"]:
                op["security"] = [{"bearerAuth": []}]
            item[ep["method"].lower()] = op
            total += 1

    spec = {
        "openapi": "3.0.3",
        "info": {
            "title": title,
            "version": version,
            "description": "Spec generado automáticamente desde el código (análisis estático de routers Express). "
                           "Revisar y enriquecer parámetros/esquemas manualmente. / "
                           "Auto-generated from code (static analysis of Express routers). "
                           "Review and enrich parameters/schemas manually.",
        },
        "tags": [{"name": k} for k in sorted(tags)],
        "components": {
            "securitySchemes": {
                "bearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
            }
        },
        "paths": dict(sorted(paths.items())),
    }
    return spec, total, len(tags)


def main():
    args = sys.argv[1:]
    if not args:
        print("Uso: python3 generate_openapi.py <repo_path> [--entry ...] [--out ...] [--title ...]")
        sys.exit(1)
    repo = os.path.abspath(args[0])
    entry = None
    out = None
    title = None
    version = "1.0.0"
    i = 1
    while i < len(args):
        if args[i] == "--entry":
            entry = os.path.join(repo, args[i + 1]); i += 2
        elif args[i] == "--out":
            out = args[i + 1]; i += 2
        elif args[i] == "--title":
            title = args[i + 1]; i += 2
        elif args[i] == "--version":
            version = args[i + 1]; i += 2
        else:
            i += 1

    pkg = {}
    pkgp = os.path.join(repo, "package.json")
    if os.path.isfile(pkgp):
        try:
            pkg = json.load(open(pkgp, encoding="utf-8"))
        except Exception:
            pkg = {}
    title = title or (pkg.get("name", "API") + " — API Reference")
    version = pkg.get("version", version)

    entry = entry or find_entry(repo)
    if not entry or not os.path.isfile(entry):
        print(json.dumps({"error": "No se encontró el archivo de arranque (app.ts/app.js)."}))
        sys.exit(2)

    spec, total, ntags = to_openapi(repo, entry, title, version)

    out = out or os.path.join(repo, "docs", "openapi.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2, ensure_ascii=False)

    print(json.dumps({
        "ok": True,
        "entry": entry,
        "output": out,
        "endpoints": total,
        "tags": ntags,
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
