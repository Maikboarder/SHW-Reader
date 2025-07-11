# Crear Release en GitHub - SHW Reader v1.0.0

## Archivos para subir al release:

### Windows:
- `SHW Reader Setup 1.0.0.exe` - Instalador principal de Windows
- `SHW Reader 1.0.0.exe` - Ejecutable portable de Windows

### macOS:
- `SHW Reader-1.0.0.dmg` - Instalador para macOS Intel
- `SHW Reader-1.0.0-arm64.dmg` - Instalador para macOS Apple Silicon (M1/M2)
- `SHW Reader-1.0.0-mac.zip` - Archivo comprimido para macOS Intel
- `SHW Reader-1.0.0-arm64-mac.zip` - Archivo comprimido para macOS Apple Silicon

## Pasos para crear el release:

### 1. Ir a GitHub Releases
1. Ve a tu repositorio en GitHub
2. Haz clic en "Releases" (en la sidebar derecha o en la pestaña)
3. Haz clic en "Create a new release"

### 2. Configurar el release
- **Tag version**: `v1.0.0`
- **Release title**: `SHW Reader v1.0.0 - Embedded Backend`
- **Target**: `main` (rama principal)

### 3. Descripción del release (copiar esto):

```
# SHW Reader v1.0.0 - Backend Embebido

🎉 **Nueva versión completamente autónoma** - ¡No requiere instalación de Python!

## 🆕 Nuevas características

- ✅ **Backend Flask completamente embebido** - No necesitas Python instalado
- ✅ **Funcionamiento autónomo** - La app funciona sin dependencias externas
- ✅ **Modo de respaldo mejorado** - Si algo falla, tendrás funcionalidad básica
- ✅ **Mejor manejo de errores** - Mensajes claros y útiles para el usuario
- ✅ **Soporte mejorado para Windows y macOS**

## 📥 Descargas

### Windows
- **`SHW Reader Setup 1.0.0.exe`** - Instalador recomendado (con instalación automática)
- **`SHW Reader 1.0.0.exe`** - Ejecutable portable (no requiere instalación)

### macOS
- **`SHW Reader-1.0.0.dmg`** - Para Mac con procesador Intel
- **`SHW Reader-1.0.0-arm64.dmg`** - Para Mac con Apple Silicon (M1/M2)
- **`SHW Reader-1.0.0-mac.zip`** - Archivo comprimido para Intel Mac
- **`SHW Reader-1.0.0-arm64-mac.zip`** - Archivo comprimido para Apple Silicon

## 🔧 Cambios técnicos

- Eliminación completa de dependencias externas de Python
- Backend Flask compilado como ejecutable embebido
- Servidor de respaldo en Node.js para casos de emergencia
- Mejora significativa en la estabilidad y confiabilidad

## 📋 Requisitos del sistema

- **Windows**: Windows 10 o superior
- **macOS**: macOS 10.14 o superior

## 🐛 Resolución de problemas

Si encuentras algún problema, consulta el archivo `TROUBLESHOOTING.md` en el repositorio.

---

**Nota**: Esta versión reemplaza completamente las versiones anteriores y resuelve todos los problemas de dependencias externas.
```

### 4. Subir los archivos
1. Arrastra y suelta los siguientes archivos desde la carpeta `dist/`:
   - `SHW Reader Setup 1.0.0.exe`
   - `SHW Reader 1.0.0.exe`
   - `SHW Reader-1.0.0.dmg`
   - `SHW Reader-1.0.0-arm64.dmg`
   - `SHW Reader-1.0.0-mac.zip`
   - `SHW Reader-1.0.0-arm64-mac.zip`

### 5. Publicar
1. Marca "Set as the latest release"
2. Haz clic en "Publish release"

## ✅ Verificación post-release

Después de publicar:
1. Verifica que todos los archivos se subieron correctamente
2. Prueba descargar uno de los instaladores
3. Actualiza el README.md con enlaces a la nueva versión

## 📝 Actualizar documentación

Considera actualizar:
- README.md con enlaces al nuevo release
- INSTALLATION.md con instrucciones actualizadas
- Cualquier documentación que mencione versiones anteriores
