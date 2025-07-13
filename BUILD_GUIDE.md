
# Guía de compilación

## Requisitos

- Node.js 18+
- npm
- macOS 10.15+ (Apple Silicon o Intel)

## Pasos para compilar

1. Instala dependencias: `npm install`
2. Genera el backend standalone: `sh build_flask_mac_arm64.sh`
3. Empaqueta la app: `npm run build:mac-silicon`
4. El instalador estará en la carpeta `dist/`
