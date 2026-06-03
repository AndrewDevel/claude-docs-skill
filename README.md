# claude-docs-skill

Marketplace de Claude con un plugin para **documentar proyectos de desarrollo** de forma automática,
bilingüe (español/inglés) y mantenible en el tiempo.
_A Claude marketplace with a plugin to automatically document developer projects — bilingual (ES/EN)
and maintainable over time._

---

## ¿Qué hace? / What it does

El plugin **`project-docs`** detecta el stack de un repositorio y genera/mantiene su documentación
dentro de la carpeta `/docs` del propio repo, servida como un sitio navegable con **Docusaurus**.

Genera hasta tres tipos de documentación, **según aplique** al repo:

| Tipo | Contenido | ¿Cuándo? |
| ---- | --------- | -------- |
| **Técnica** | Arquitectura, decisiones de diseño, setup del entorno, estructura del repo, modelos de datos | Siempre |
| **Guía de plataforma** | Onboarding y flujos paso a paso para el cliente final | Repos con UI (frontend / full-stack / móvil) |
| **Referencia de API** | Endpoints, autenticación, contratos | Repos que exponen una API |

**Detección automática de stack:** frontend (Angular/React/Vue), backend/API (Express/NestJS/Fastify),
full-stack, y apps móviles Swift/iOS (Package.swift, .xcodeproj, Podfile → DocC de Apple).

**Referencia de API con fallback inteligente:**
1. Si el backend expone **OpenAPI/Swagger** → se embebe con Scalar o Redoc.
2. Si **no** hay Swagger → se **genera el spec OpenAPI analizando los routers/controllers** del código.
3. Si nada aplica → referencia en **Markdown estructurado**.
4. Swift/iOS → **DocC**.

Todo el contenido es **bilingüe (ES/EN)** e incluye un workflow de despliegue a **GitHub Pages**.

---

## Instalar / Install

En Claude Code o Cowork, agrega este marketplace y luego instala el plugin.

```bash
# 1. Agregar el marketplace (desde GitHub, una vez publicado)
/plugin marketplace add AndrewDevel/claude-docs-skill

# 2. Instalar el plugin
/plugin install project-docs@claude-docs-skill
```

> Mientras el repo aún es local (sin push), puedes agregarlo por ruta:
> `/plugin marketplace add /ruta/a/claude-docs-skill`

Verifica con `/plugin marketplace list` y `/help` (deberían aparecer los comandos `docs-*`).

---

## Uso / Usage

El plugin expone cuatro comandos de ciclo de vida. Todos aceptan la ruta del repo como argumento
(o usan el directorio actual si se omite):

| Comando | Qué hace |
| ------- | -------- |
| `/docs-init [ruta]` | Inicializa la documentación: detecta el stack, hace scaffolding de Docusaurus, genera contenido bilingüe inicial y el workflow de GitHub Pages. |
| `/docs-update [ruta]` | Actualiza/regenera la documentación tras cambios en el código, editando solo lo afectado. |
| `/docs-api [ruta]` | Genera o actualiza la referencia de API (con la lógica de fallback). |
| `/docs-validate [ruta]` | Valida que los docs estén completos y al día (placeholders, sincronía de API, versión, bilingüismo). |

También puedes simplemente pedirle a Claude “documenta este repo” y el skill `project-docs` se activará.

### Ejemplo / Example

```text
/docs-init ./pp_ws_api_core
```

Claude detecta que es un backend Express en TypeScript sin Swagger, hace scaffolding del sitio
Docusaurus en `pp_ws_api_core/docs`, escribe la documentación técnica bilingüe y genera la referencia
de API a partir del análisis estático de los routers.

### Correr el sitio localmente / Run the site locally

```bash
cd <repo>/docs
npm install
npm run start     # http://localhost:3000
```

### Desplegar / Deploy

El comando `docs-init` copia un workflow a `<repo>/.github/workflows/deploy-docs.yml`. Activa
**Settings → Pages → Source = GitHub Actions** en el repo y cada push a `main` que toque `docs/`
publicará el sitio.

---

## Estructura del repo / Repo structure

```
claude-docs-skill/
├── .claude-plugin/
│   └── marketplace.json            # define el marketplace y lista el plugin
├── plugins/
│   └── project-docs/
│       ├── .claude-plugin/plugin.json
│       ├── commands/               # 4 slash commands del ciclo de vida
│       │   ├── docs-init.md
│       │   ├── docs-update.md
│       │   ├── docs-api.md
│       │   └── docs-validate.md
│       ├── skills/project-docs/
│       │   ├── SKILL.md
│       │   ├── references/         # docusaurus, api-reference, docc, mkdocs
│       │   ├── scripts/            # detect_stack.py, generate_openapi.py
│       │   └── assets/             # plantillas Docusaurus + Markdown bilingües + workflow
│       └── README.md
└── README.md
```

---

## Alternativa documentada / Documented alternative

MkDocs Material está documentado como alternativa a Docusaurus en
`plugins/project-docs/skills/project-docs/references/mkdocs-alternative.md`. Docusaurus es la base por
defecto por encajar con stacks Node/React.

## Licencia / License

MIT — ver [LICENSE](./LICENSE).
