# DocC para proyectos Swift / iOS

Cuando el detector devuelve `repo_type: mobile-swift`, la referencia de código se genera con
**DocC**, la herramienta oficial de Apple. Es más técnica y se complementa con la guía de plataforma.

## Detección

El repo se clasifica como `mobile-swift` si existe `Package.swift`, `*.xcodeproj`, `*.xcworkspace`,
`Podfile`, o archivos `.swift`.

## Generar el archivo DocC

**Swift Package Manager:**

```bash
swift package --allow-writing-to-directory ./docs \
  generate-documentation --target <Target> \
  --output-path ./docs/static/docc \
  --transform-for-static-hosting \
  --hosting-base-path <GH_REPO>
```

**Proyecto Xcode (xcodebuild):**

```bash
xcodebuild docbuild -scheme <Scheme> -derivedDataPath ./dd
# El .doccarchive queda en ./dd/Build/Products/.../<Target>.doccarchive
xcrun docc process-archive transform-for-static-hosting \
  <Target>.doccarchive --output-path ./docs/static/docc \
  --hosting-base-path <GH_REPO>
```

## Integración con Docusaurus

DocC produce un sitio estático propio. Dos opciones:

1. **Enlace embebido:** copiar la salida a `docs/static/docc/` y enlazarla desde una página de la
   sección API (`docs/docs/api/codigo.md`) con un `<iframe>` o un enlace directo a `/docc/`.
2. **Sitio separado:** publicar el DocC archive en una subruta de GitHub Pages.

Documentar en español e inglés cómo regenerar el DocC cuando cambie el código del app.

## Qué documentar además del DocC

- **Técnica:** estructura del proyecto (targets, módulos, capas), gestión de dependencias
  (SPM/CocoaPods), configuración de entornos (schemes, `.xcconfig`), modelos de datos.
- **Plataforma:** onboarding y flujos de las pantallas principales del app, con capturas si es posible.
