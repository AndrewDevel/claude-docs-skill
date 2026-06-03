#!/usr/bin/env python3
"""
detect_stack.py — Detecta el tipo de repositorio y propone los entregables de
documentación. / Detects repository type and proposes documentation deliverables.

Solo usa la librería estándar de Python (sin dependencias).
Stdlib only — no dependencies.

Uso / Usage:
    python3 detect_stack.py <ruta_del_repo>
    python3 detect_stack.py <repo_path> --json   # salida JSON pura

Salida: JSON con la clasificación del repo y recomendaciones.
"""
import json
import os
import re
import sys
import glob


def read_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def exists(repo, *names):
    """True si alguno de los nombres/patrones existe en la raíz del repo."""
    for n in names:
        if glob.glob(os.path.join(repo, n)):
            return True
    return False


def deep_glob(repo, pattern, limit=1):
    """Busca un patrón recursivamente ignorando node_modules/.git/build."""
    found = []
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in (
            "node_modules", ".git", "build", "dist", ".angular", "Pods", "vendor")]
        for f in files:
            if re.search(pattern, f):
                found.append(os.path.join(root, f))
                if len(found) >= limit:
                    return found
    return found


def detect_node(repo, pkg):
    deps = {}
    deps.update(pkg.get("dependencies", {}) or {})
    deps.update(pkg.get("devDependencies", {}) or {})
    dep_names = set(deps.keys())

    frontend_markers = {
        "@angular/core": "Angular",
        "react": "React",
        "react-dom": "React",
        "vue": "Vue",
        "next": "Next.js",
        "@nuxt/core": "Nuxt",
        "svelte": "Svelte",
    }
    backend_markers = {
        "express": "Express",
        "@nestjs/core": "NestJS",
        "fastify": "Fastify",
        "koa": "Koa",
        "@hapi/hapi": "Hapi",
        "apollo-server": "Apollo GraphQL",
    }

    frontend_fw = sorted({v for k, v in frontend_markers.items() if k in dep_names})
    backend_fw = sorted({v for k, v in backend_markers.items() if k in dep_names})

    # Angular también se detecta por angular.json
    if exists(repo, "angular.json") and "Angular" not in frontend_fw:
        frontend_fw.append("Angular")

    has_frontend = bool(frontend_fw)
    has_backend = bool(backend_fw)

    if has_frontend and has_backend:
        repo_type = "fullstack"
    elif has_backend:
        repo_type = "backend"
    elif has_frontend:
        repo_type = "frontend"
    else:
        # Heurística: main apunta a un server, o hay carpeta de rutas
        main = (pkg.get("main") or "") + " " + json.dumps(pkg.get("scripts", {}))
        if re.search(r"server|app\.(js|ts)|src/app", main) or deep_glob(repo, r"\.router\.(t|j)s$"):
            repo_type = "backend"
            has_backend = True
        else:
            repo_type = "node"

    language = "TypeScript" if exists(repo, "tsconfig.json") or "typescript" in dep_names else "JavaScript"

    return repo_type, frontend_fw, backend_fw, language, dep_names


def detect_openapi(repo, dep_names):
    """Determina la estrategia de referencia de API (fallback a-b-c)."""
    swagger_deps = {
        "swagger-ui-express", "@nestjs/swagger", "@fastify/swagger",
        "fastify-swagger", "swagger-jsdoc", "redoc-express", "express-openapi",
        "tsoa",
    }
    if dep_names & swagger_deps:
        return {
            "strategy": "embed",
            "reason": "El backend ya expone OpenAPI/Swagger (dependencia detectada).",
            "deps": sorted(dep_names & swagger_deps),
        }
    # Especificación existente en archivos
    spec = deep_glob(repo, r"(openapi|swagger)\.(json|ya?ml)$", limit=1)
    if spec:
        return {"strategy": "embed", "reason": "Se encontró un spec OpenAPI existente.", "spec": spec[0]}
    # ¿Hay rutas Express analizables?
    if deep_glob(repo, r"\.router\.(t|j)s$") or deep_glob(repo, r"routes?\.(t|j)s$"):
        return {
            "strategy": "generate-from-code",
            "reason": "No hay Swagger; se generará el spec OpenAPI analizando los routers/controllers.",
        }
    return {
        "strategy": "markdown",
        "reason": "No se detectó API analizable; se generará referencia en Markdown estructurado.",
    }


def detect_mobile(repo):
    if exists(repo, "Package.swift", "*.xcodeproj", "*.xcworkspace", "Podfile") or deep_glob(repo, r"\.swift$"):
        return {
            "repo_type": "mobile-swift",
            "language": "Swift",
            "frameworks": ["Swift / Xcode"],
            "api_reference": {
                "strategy": "docc",
                "reason": "Proyecto Swift/iOS: usar DocC de Apple para la referencia de código.",
            },
            "doc_types": ["technical", "platform-guide", "docc-reference"],
        }
    return None


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    repo = os.path.abspath(args[0]) if args else "."
    if not os.path.isdir(repo):
        print(json.dumps({"error": f"No existe el directorio: {repo}"}))
        sys.exit(1)

    # 1) Mobile / Swift primero
    mobile = detect_mobile(repo)
    if mobile:
        result = {"repo": repo}
        result.update(mobile)
        result["docs_dir"] = os.path.join(repo, "docs")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    # 2) Node / JS
    pkg = read_json(os.path.join(repo, "package.json"))
    if pkg:
        repo_type, fe, be, lang, deps = detect_node(repo, pkg)
        result = {
            "repo": repo,
            "name": pkg.get("name"),
            "repo_type": repo_type,
            "language": lang,
            "frameworks": fe + be,
            "frontend_frameworks": fe,
            "backend_frameworks": be,
        }
        if repo_type in ("backend", "fullstack"):
            result["api_reference"] = detect_openapi(repo, deps)
        # Tipos de documentación recomendados
        doc_types = ["technical"]
        if repo_type in ("frontend", "fullstack"):
            doc_types.append("platform-guide")
        if repo_type in ("backend", "fullstack"):
            doc_types.append("api-reference")
        result["doc_types"] = doc_types
        result["docs_site"] = "docusaurus"
        result["docs_dir"] = os.path.join(repo, "docs")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    # 3) Desconocido
    print(json.dumps({
        "repo": repo,
        "repo_type": "unknown",
        "note": "No se encontró package.json ni proyecto Swift. Inspeccionar manualmente.",
        "docs_dir": os.path.join(repo, "docs"),
        "doc_types": ["technical"],
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
