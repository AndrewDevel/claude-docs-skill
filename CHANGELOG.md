# Changelog

Todas las versiones notables del marketplace `claude-docs-skill` y del plugin `project-docs`.
Formato basado en [Keep a Changelog](https://keepachangelog.com/), versionado [SemVer](https://semver.org/).

> Al publicar una versión: sube el número en `.claude-plugin/marketplace.json`,
> `plugins/project-docs/.claude-plugin/plugin.json` y el `metadata.version` del `SKILL.md`,
> luego en Claude Code: `/plugin marketplace update claude-docs-skill` →
> `/plugin install project-docs@claude-docs-skill` → `/reload-plugins`.

## [0.2.0] — 2026-06-03

### Añadido
- Tema Docusaurus con la **identidad de marca PagaCel** (slate `#2D3142`, acento `#7366ff`,
  cyan `#00B4D8`), modo claro/oscuro, announcement bar y sidebar colapsable.
- Favicon y logo de marca (`pagacel-icon`) + lógica para reutilizar el logo propio de cada repo.
- Mermaid habilitado; plantillas `.mdx` con **pestañas ES/EN**, admonitions y diagramas
  (flowchart / sequence / ER / mindmap).
- Nuevas plantillas: **testing** (pirámide de pruebas, cobertura, casos críticos),
  **troubleshooting** (FAQ) y **changelog** de documentación.
- Referencia `rich-content.md` (catálogo de componentes visuales/interactivos).
- `SKILL.md` y los comandos ahora exigen contenido enriquecido (no plano); `docs-validate`
  marca ⚠️ las páginas sin elementos visuales.

## [0.1.0] — 2026-06-03

### Añadido
- Marketplace `claude-docs-skill` con el plugin `project-docs`.
- Skill que detecta el stack (frontend / backend / full-stack / Swift) y genera documentación
  bilingüe con Docusaurus.
- Scripts sin dependencias: `detect_stack.py` y `generate_openapi.py` (OpenAPI desde routers Express).
- Comandos de ciclo de vida: `/docs-init`, `/docs-update`, `/docs-api`, `/docs-validate`.
- Referencia de API con fallback (embed Swagger → generar desde código → DocC → Markdown).
- Workflow de despliegue a GitHub Pages.
