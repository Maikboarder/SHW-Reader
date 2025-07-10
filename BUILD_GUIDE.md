# Guía de Compilación - SHW Reader para macOS

## Prerequisitos

1. **Node.js** (versión 16 o superior)
2. **Python 3** con pip
3. **Xcode Command Line Tools**:
   ```bash
   xcode-select --install
   ```

## Instalación de Dependencias

```bash
# Instalar dependencias de Node.js
npm install

# Instalar dependencias de Python
pip3 install -r requirements.txt
```

## Opciones de Compilación

### 1. Compilación Automática (Recomendado)
```bash
./build-macos.sh
```
Este script compila automáticamente para Intel y Apple Silicon.

### 2. Compilaciones Individuales

#### Intel (x64)
```bash
npm run dist:mac-intel
```

#### Apple Silicon (arm64)
```bash
npm run dist:mac-silicon
```

#### Universal (Intel + Apple Silicon en un solo archivo)
```bash
npm run dist:mac-universal
```

#### Ambas arquitecturas por separado
```bash
npm run dist:mac
```

### 3. Solo Empaquetado (sin instalador)
```bash
npm run pack
```

## Archivos Generados

Los archivos compilados se guardan en el directorio `dist/`:

- **DMG (Instalador)**: `SHW Reader-1.0.0-mac-x64.dmg` / `SHW Reader-1.0.0-mac-arm64.dmg`
- **ZIP (Aplicación)**: `SHW Reader-1.0.0-mac-x64.zip` / `SHW Reader-1.0.0-mac-arm64.zip`

## Arquitecturas Soportadas

- **Intel (x64)**: Compatible con Macs Intel (2006-2020)
- **Apple Silicon (arm64)**: Compatible con Macs M1/M2/M3 (2020+)
- **Universal**: Un solo archivo compatible con ambas arquitecturas

## Configuración de Firma (Opcional)

Para distribuir la aplicación fuera del App Store, necesitas configurar la firma de código:

1. Obtén un certificado de desarrollador de Apple
2. Configura las variables de entorno:
   ```bash
   export CSC_IDENTITY_AUTO_DISCOVERY=false
   export CSC_IDENTITY="Developer ID Application: Tu Nombre (TEAM_ID)"
   ```

## Resolución de Problemas

### Error: "Cannot find module electron-builder"
```bash
npm install --save-dev electron-builder
```

### Error de permisos en Python
```bash
pip3 install --user -r requirements.txt
```

### Error: "Command not found: xcode-select"
Instala Xcode Command Line Tools:
```bash
xcode-select --install
```

## Estructura de Archivos Incluidos

La aplicación incluye automáticamente:
- `electron-main.js` - Proceso principal de Electron
- `preload.js` - Script de preload
- `app_desktop.py` - Servidor Flask backend
- `templates/` - Plantillas HTML
- `static/` - Archivos estáticos (CSS, JS, imágenes)
- `translations/` - Archivos de traducción (9 idiomas)
- `assets/` - Iconos y recursos de la aplicación
- `requirements.txt` - Dependencias de Python
