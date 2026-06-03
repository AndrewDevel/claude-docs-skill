---
description: Genera o actualiza la referencia de API (OpenAPI con fallback)
argument-hint: "[ruta-del-repo]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(python3:*), Bash(ls:*), Bash(find:*)
---

Genera o actualiza la referencia de API de un repo. / Generate or update a repo's API reference.

Repo objetivo / target repo: `$1` (si está vacío, usa el directorio actual).

Sigue la lógica de fallback descrita en
`${CLAUDE_PLUGIN_ROOT}/skills/project-docs/references/api-reference.md`:

1. Detecta la estrategia: `python3 ${CLAUDE_PLUGIN_ROOT}/skills/project-docs/scripts/detect_stack.py $1`
   y lee `api_reference.strategy`.

2. Según la estrategia:
   - **embed** → embebe el OpenAPI/Swagger existente con Scalar o Redoc.
   - **generate-from-code** → ejecuta
     `python3 ${CLAUDE_PLUGIN_ROOT}/skills/project-docs/scripts/generate_openapi.py $1 --out $1/docs/static/openapi.json`
     y embébelo con Scalar/Redoc (plantilla `assets/templates/api-reference.mdx`). Avisa que es un
     borrador derivado del código y enriquece parámetros/esquemas leyendo los validators si conviene.
   - **docc** → genera DocC (ver `references/mobile-docc.md`).
   - **markdown** → escribe la referencia a mano con `assets/templates/api-reference-markdown.md`.

3. Reporta cuántos endpoints/tags se documentaron y dónde quedó el archivo. No comitees.
