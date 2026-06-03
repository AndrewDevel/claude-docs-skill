---
description: Actualiza/regenera la documentación cuando el código cambió
argument-hint: "[ruta-del-repo]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(python3:*), Bash(git:*), Bash(ls:*), Bash(find:*)
---

Actualiza la documentación existente de un repo tras cambios en el código. / Update existing docs after code changes.

Repo objetivo / target repo: `$1` (si está vacío, usa el directorio actual).

Sigue el flujo del skill **project-docs** (paso "actualizar"):

1. Re-detecta el stack: `python3 ${CLAUDE_PLUGIN_ROOT}/skills/project-docs/scripts/detect_stack.py $1`.

2. Identifica qué cambió desde la última documentación. Si hay git, usa
   `!git -C $1 log --oneline -15` y `!git -C $1 diff --stat HEAD~10..HEAD` como pistas de qué módulos,
   rutas o modelos se tocaron. Compara contra el contenido actual en `$1/docs/docs/`.

3. Edita **solo las secciones afectadas** de los documentos técnicos / de plataforma, preservando la
   prosa escrita por humanos. No regeneres todo desde cero.

4. Si el repo expone API, refresca la referencia ejecutando `/docs-api $1`.

5. Actualiza la línea "Última actualización / Last updated" y la versión (desde `package.json`).

6. Reporta un resumen conciso de qué secciones se actualizaron. No comitees.
