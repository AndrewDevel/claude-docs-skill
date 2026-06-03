# project-docs

Plugin de Claude para generar y mantener documentación bilingüe (ES/EN) de proyectos de desarrollo
con Docusaurus. _Claude plugin to generate and maintain bilingual developer documentation._

## Componentes / Components

- **Skill `project-docs`** — conocimiento del flujo de documentación, detección de stack, plantillas
  y scripts. Se activa cuando pides documentar, actualizar o validar la documentación de un repo.
- **Comandos / Commands:**
  - `/docs-init [ruta]` — inicializa la documentación de un repo.
  - `/docs-update [ruta]` — actualiza los docs tras cambios en el código.
  - `/docs-api [ruta]` — genera/actualiza la referencia de API (OpenAPI con fallback).
  - `/docs-validate [ruta]` — valida que los docs estén completos y al día.

## Scripts (sin dependencias / dependency-free)

- `skills/project-docs/scripts/detect_stack.py <repo>` — clasifica el repo (frontend/backend/full-stack/
  Swift) y propone los entregables y la estrategia de API.
- `skills/project-docs/scripts/generate_openapi.py <repo> [--entry ...] [--out ...]` — genera un spec
  OpenAPI 3.0 analizando estáticamente los routers de Express.

Ambos usan solo la librería estándar de Python 3.

## Setup

No requiere variables de entorno. Para correr el sitio generado se necesita Node ≥ 18 (Docusaurus).
Los scripts requieren Python 3.

## Detección de stack / Stack detection

| Marcadores | Resultado |
| ---------- | --------- |
| `@angular/core` / `angular.json` | frontend (Angular) |
| `react` / `vue` / `next` | frontend |
| `express` / `@nestjs/core` / `fastify` | backend |
| frontend + backend | full-stack |
| `Package.swift` / `.xcodeproj` / `Podfile` / `.swift` | mobile-swift (DocC) |

## Estrategia de referencia de API / API reference strategy

`embed` (Swagger existente) → `generate-from-code` (analizar routers) → `markdown` (fallback) ·
`docc` para Swift. Detalle en `skills/project-docs/references/api-reference.md`.
