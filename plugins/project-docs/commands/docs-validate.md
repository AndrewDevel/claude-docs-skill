---
description: Valida que la documentación esté completa y al día con el código
argument-hint: "[ruta-del-repo]"
allowed-tools: Read, Glob, Grep, Bash(python3:*), Bash(ls:*), Bash(find:*), Bash(diff:*)
---

Valida que la documentación de un repo esté completa y sincronizada con el código.
Validate that a repo's documentation is complete and in sync with the code.

Repo objetivo / target repo: `$1` (si está vacío, usa el directorio actual).

Realiza estas comprobaciones y reporta un checklist conciso (✅/⚠️/❌):

1. Detecta el stack: `python3 ${CLAUDE_PLUGIN_ROOT}/skills/project-docs/scripts/detect_stack.py $1`.
   ¿Existe una sección para **cada** `doc_type` aplicable en `$1/docs/docs/`?

2. **Sincronía de API**: si aplica, regenera el spec a un temporal
   `python3 ${CLAUDE_PLUGIN_ROOT}/skills/project-docs/scripts/generate_openapi.py $1 --out /tmp/_openapi_check.json`
   y compara el número de endpoints/paths contra `$1/docs/static/openapi.json`. Reporta diferencias.

3. **Placeholders**: busca placeholders `{{...}}` sin rellenar en `$1/docs` (con Grep). Cualquier
   coincidencia es ❌.

4. **Versión**: compara la versión en las páginas con la de `$1/package.json`. Desincronía = ⚠️.

5. **Bilingüe**: verifica que las páginas tengan secciones en español E inglés (o archivos espejo i18n).

6. **Riqueza / no plano**: revisa que las páginas usen elementos visuales (al menos un diagrama Mermaid
   o tabla, y admonitions). Páginas sin ningún elemento visual = ⚠️ "documentación plana".

No modifiques nada. Solo reporta y, al final, ofrece ejecutar `/docs-update $1` para corregir.
