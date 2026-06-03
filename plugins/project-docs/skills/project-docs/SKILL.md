---
name: project-docs
description: >
  Genera y mantiene documentación de proyectos de desarrollo (bilingüe español/inglés)
  dentro de la carpeta /docs de cada repo, usando Docusaurus como sitio navegable.
  This skill should be used whenever the user wants to "document a repo", "documentar un proyecto",
  "generar documentación técnica", "crear una guía de plataforma para el cliente", "generar la
  referencia de API", "set up Docusaurus docs", "actualizar la documentación", or asks to scaffold,
  initialize, update, or validate developer documentation for a frontend (Angular/React/Vue),
  a backend/API (Express/NestJS/Fastify), a full-stack repo, or a Swift/iOS mobile app. It detects
  the stack automatically and produces technical docs, end-user platform guides, and an API
  reference (embedding existing OpenAPI, generating OpenAPI from code, DocC for Swift, or structured
  Markdown as fallback). Use it proactively any time documentation needs to be created or kept up to date.
metadata:
  version: "0.1.0"
  author: "AndrewDevel"
---

# Project Docs — Documentación de proyectos / Developer documentation

Genera y **mantiene** documentación viva para repos de desarrollo. Todo el contenido se escribe
**bilingüe (español + inglés)** y vive dentro de `/<repo>/docs`, servido con **Docusaurus**.

This skill produces up to three documentation types, **only those that apply** to the detected repo:

1. **Technical (interna)** — arquitectura, decisiones de diseño, setup del entorno, estructura del
   repo, modelos de datos. _Architecture, design decisions, environment setup, repo structure, data models._
2. **Platform guide (cliente final)** — onboarding y flujos paso a paso de la plataforma.
   _End-user onboarding and step-by-step flows._ (Solo para repos con UI: frontend / full-stack / móvil.)
3. **API reference** — solo si el proyecto expone una API. _Only if the project exposes an API._

## Workflow

The skill is invoked directly or through the plugin's lifecycle commands:
`/docs-init`, `/docs-update`, `/docs-api`, `/docs-validate`. Whatever the entry point, follow this loop.

### Step 1 — Detect the stack (always first)

Run the detector and read its JSON. It tells you the repo type, language, frameworks, which doc
types apply, and the API-reference strategy.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/project-docs/scripts/detect_stack.py <repo_path>
```

Repo types: `frontend`, `backend`, `fullstack`, `mobile-swift`, `node`, `unknown`.
Map the `doc_types` field to what you'll generate:

| repo_type      | technical | platform-guide | api-reference            |
| -------------- | --------- | -------------- | ------------------------ |
| frontend       | ✅        | ✅             | —                        |
| backend        | ✅        | —              | ✅                       |
| fullstack      | ✅        | ✅             | ✅                       |
| mobile-swift   | ✅        | ✅             | ✅ (DocC, see reference) |

Confirm the plan with the user before writing files if anything is ambiguous (e.g. a repo that
could be either backend-only or full-stack).

### Step 2 — Scaffold the docs site (init only)

If `/<repo>/docs` has no Docusaurus site yet, scaffold one. Read
`references/docusaurus.md` for the exact files, then copy and fill the templates from
`assets/docusaurus/` and `assets/templates/`. Always include the GitHub Pages deploy workflow from
`assets/workflows/deploy-docs.yml`. MkDocs Material is documented as an alternative in
`references/mkdocs-alternative.md` — only use it if the user explicitly asks.

The site must expose three sidebar sections that mirror the doc types (Técnica / Guía de plataforma /
API), each written in Spanish and English. Use Docusaurus i18n (`es` default, `en` locale) as
described in the reference.

### Step 3 — Generate / refresh content

For each applicable doc type, write Markdown into `/<repo>/docs/docs/` using the bilingual templates
in `assets/templates/`:

- `technical.md` → llena con arquitectura real inferida del código (estructura de carpetas, módulos,
  rutas/feature folders, modelos de datos, variables de entorno, comandos de build/test).
- `platform-guide.md` → describe los flujos de usuario observados en las vistas/pantallas.
- Fill placeholders (`{{...}}`) with facts gathered by reading the repo — never leave template
  placeholders in the final output.

When **updating** (not initializing), diff what changed in the code (new routes, new modules, new
env vars, version bumps) and edit only the affected sections, preserving human-written prose. Bump
the "última actualización / last updated" line.

### Step 4 — API reference (when applicable)

Follow the fallback logic. The detector's `api_reference.strategy` field tells you which branch:

- **`embed`** — the backend already exposes OpenAPI/Swagger, or a spec file exists. Embed it in the
  site with **Scalar** or **Redoc** (see `references/api-reference.md`).
- **`generate-from-code`** — no Swagger. Generate the spec from the source:

  ```bash
  python3 ${CLAUDE_PLUGIN_ROOT}/skills/project-docs/scripts/generate_openapi.py <repo_path> \
      --out <repo_path>/docs/static/openapi.json
  ```

  Then embed that generated `openapi.json` with Scalar/Redoc. Tell the user the spec is a code-derived
  draft to review (parameters and schemas are inferred minimally).

- **`docc`** — Swift/iOS. Use Apple's DocC (see `references/mobile-docc.md`).
- **`markdown`** — nothing analyzable. Hand-write a structured Markdown API reference from the route
  table you can read in the code.

Read `references/api-reference.md` before doing any of these — it has the exact embed snippets.

### Step 5 — Validate (validate command)

Check the docs are up to date relative to the code:

- ¿Existen secciones para cada `doc_type` aplicable?
- ¿El número de rutas en el código coincide con el `openapi.json`? (re-run the generator to a temp
  file and diff endpoint counts.)
- ¿Hay placeholders `{{...}}` sin llenar? ¿Versiones desincronizadas con `package.json`?
- Report a concise checklist of what's stale and offer to fix it.

## Reference files

Read these on demand — don't load them all at once:

- `references/docusaurus.md` — scaffolding, i18n bilingüe, sidebars, deploy a GitHub Pages.
- `references/api-reference.md` — Scalar/Redoc embed, fallback OpenAPI desde código.
- `references/mobile-docc.md` — DocC para proyectos Swift/iOS.
- `references/mkdocs-alternative.md` — alternativa MkDocs Material (solo si el usuario la pide).

## Scripts

- `scripts/detect_stack.py <repo>` — clasifica el repo y propone entregables (stdlib, sin deps).
- `scripts/generate_openapi.py <repo> [--entry ...] [--out ...]` — genera OpenAPI 3.0 desde routers
  Express (stdlib, sin deps).

## Bilingual writing rule

Every page is bilingual. Prefer one of two patterns and be consistent within a repo:
(a) two stacked sections per page (`## Español` / `## English`), or (b) Docusaurus i18n with mirrored
`es`/`en` files. The templates in `assets/templates/` use pattern (a) by default because it survives
even if i18n is not configured. Never ship a page that exists in only one language.
