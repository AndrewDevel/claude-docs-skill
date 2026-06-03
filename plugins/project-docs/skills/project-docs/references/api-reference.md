# Referencia de API — lógica de fallback / API reference fallback logic

El detector entrega `api_reference.strategy`. Sigue la rama correspondiente.

## (a) `embed` — el backend ya expone OpenAPI/Swagger

Si hay un `openapi.json` / `swagger.json` / `openapi.yaml`, o una dependencia como
`swagger-ui-express`, `@nestjs/swagger`, `@fastify/swagger`, embébelo en el sitio.

**Opción Scalar (recomendada, UI moderna):**

Crear `docs/docs/api/reference.mdx`:

```mdx
---
title: API Reference
---
import { ApiReferenceReact } from '@scalar/api-reference-react';
import '@scalar/api-reference-react/style.css';

<ApiReferenceReact configuration={{ spec: { url: '/openapi.json' } }} />
```

Instalar en el sitio de docs: `npm install @scalar/api-reference-react`.
Copiar el spec a `docs/static/openapi.json`.

**Opción Redoc (alternativa estable):**

```bash
npm install redoc
```

```mdx
import { RedocStandalone } from 'redoc';
<RedocStandalone specUrl="/openapi.json" />
```

## (b) `generate-from-code` — no hay Swagger, generar desde el código

Para backends Express con la convención `Router.method('/path', ...handlers, Controller.method)`
montados con `app.use('/prefix', router)`:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/project-docs/scripts/generate_openapi.py <repo> \
    --out <repo>/docs/static/openapi.json
```

El script:
- analiza el archivo de arranque (`src/app.ts` por defecto, autodetectado),
- mapea imports → archivos router → endpoints,
- arma rutas completas (prefijo + ruta), método, tag (por prefijo), `operationId`,
- marca `security: bearerAuth` cuando detecta middlewares tipo `validateToken`/`auth`.

Salida: OpenAPI 3.0.3. **Es un borrador derivado del código**: parámetros y esquemas de
request/response son mínimos. Avísalo al usuario y enriquécelo si hace falta leyendo los
validators (p.ej. esquemas Joi en `src/types/validations`) y los controllers.

Luego embébelo con Scalar/Redoc como en la opción (a).

### Enriquecer el spec (opcional pero valioso)

Si el repo usa validación (Joi, Zod, class-validator), lee esos esquemas y añade `requestBody` y
`parameters` al spec generado antes de embeberlo. Esto convierte el borrador en una referencia real.

## (c) `markdown` — nada analizable

Escribe a mano una referencia estructurada en `docs/docs/api/` a partir de la tabla de rutas que
puedas leer en el código. Formato por endpoint:

```markdown
### `POST /banking/v1/user/registerUser`

**Auth:** Bearer JWT — **Tag:** banking

| Campo | Tipo | Requerido | Descripción |
| ----- | ---- | --------- | ----------- |
| ...   | ...  | ...       | ...         |

**Respuesta 200:** ...
```

## DocC (Swift/iOS)

Ver `mobile-docc.md`.
