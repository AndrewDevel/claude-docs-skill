---
description: Inicializa la documentación bilingüe de un repo (Docusaurus + contenido)
argument-hint: "[ruta-del-repo]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(python3:*), Bash(ls:*), Bash(find:*)
---

Inicializa la documentación de un repositorio de desarrollo. / Initialize repo documentation.

Repo objetivo / target repo: `$1` (si está vacío, usa el directorio actual / if empty, use cwd).

Sigue el flujo del skill **project-docs**. Pasos:

1. Detecta el stack ejecutando:
   `python3 ${CLAUDE_PLUGIN_ROOT}/skills/project-docs/scripts/detect_stack.py $1`
   Lee el JSON y determina qué tipos de doc aplican (technical / platform-guide / api-reference).

2. Si `$1/docs` aún no tiene un sitio Docusaurus, hazle scaffolding copiando las plantillas de
   `${CLAUDE_PLUGIN_ROOT}/skills/project-docs/assets/docusaurus/` y rellenando los placeholders
   `{{...}}`. Incluye el workflow de GitHub Pages desde
   `${CLAUDE_PLUGIN_ROOT}/skills/project-docs/assets/workflows/deploy-docs.yml`.
   Lee `references/docusaurus.md` para el detalle.

3. Genera el contenido inicial bilingüe (ES/EN) usando las plantillas de
   `${CLAUDE_PLUGIN_ROOT}/skills/project-docs/assets/templates/`, llenando los placeholders con
   hechos reales leídos del código (estructura, módulos, rutas, modelos de datos, variables de entorno).

4. Si aplica referencia de API, ejecuta `/docs-api $1` (o sigue `references/api-reference.md`).

5. Reporta qué se creó, cómo correr el sitio (`cd $1/docs && npm install && npm run start`) y cómo
   desplegar a GitHub Pages.

No comitees los cambios; deja que el usuario revise. / Do not commit; let the user review.
