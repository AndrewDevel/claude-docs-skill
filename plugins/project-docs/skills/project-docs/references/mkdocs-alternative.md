# Alternativa: MkDocs Material (solo si el usuario la pide)

Docusaurus es la base por defecto. MkDocs Material es una alternativa válida si el equipo prefiere
Python en vez de Node, o quiere un setup más liviano. **No la uses salvo que el usuario lo pida.**

## Setup

```bash
pip install mkdocs-material mkdocs-static-i18n
```

`mkdocs.yml` mínimo bilingüe:

```yaml
site_name: {{PROJECT_NAME}}
theme:
  name: material
  language: es
plugins:
  - search
  - i18n:
      docs_structure: suffix
      languages:
        - locale: es
          default: true
          name: Español
        - locale: en
          name: English
nav:
  - Inicio: index.md
  - Técnica: tecnica/index.md
  - Plataforma: plataforma/index.md
  - API: api/index.md
```

Archivos bilingües por sufijo: `index.es.md` / `index.en.md`.

## Referencia de API en MkDocs

- OpenAPI embebido con el plugin `neoteroi-mkdocs` o `mkdocs-swagger-ui-tag`:
  ```yaml
  - swagger-ui-tag
  ```
  Y en una página: `<swagger-ui src="openapi.json"/>`.
- El `generate_openapi.py` del skill funciona igual; solo cambia dónde colocas el `openapi.json`.

## Correr y desplegar

```bash
mkdocs serve            # local
mkdocs build            # estático en site/
mkdocs gh-deploy        # publica a GitHub Pages (rama gh-pages)
```

## Cuándo elegir cuál

| Criterio                    | Docusaurus       | MkDocs Material |
| --------------------------- | ---------------- | --------------- |
| Stack del equipo            | Node/React ✅    | Python          |
| Componentes React en docs   | ✅               | limitado        |
| Setup mínimo                | medio            | muy simple ✅   |
| Embed OpenAPI (Scalar/Redoc)| ✅ nativo        | vía plugins     |
