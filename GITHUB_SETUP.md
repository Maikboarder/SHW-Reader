# Instrucciones para Subir a GitHub

## 1. Crear el Repositorio en GitHub

1. Ve a https://github.com
2. Haz clic en "+" → "New repository"
3. Nombre del repositorio: `SHW-Reader`
4. Descripción: `Professional SHW File Viewer and Export Tool - Multi-language Electron application`
5. **NO** marques "Initialize this repository with README" (ya tenemos uno)
6. **NO** agregues .gitignore (ya tenemos uno)
7. Selecciona "MIT License" o déjalo vacío (ya tenemos uno)
8. Haz clic en "Create repository"

## 2. Conectar el Repositorio Local con GitHub

Una vez creado el repositorio en GitHub, ejecuta estos comandos en la terminal:

```bash
# Cambiar al directorio del proyecto
cd "/Users/imaik/Documents/SHW-Reader"

# Agregar el repositorio remoto (reemplaza 'yourusername' con tu usuario de GitHub)
git remote add origin https://github.com/yourusername/SHW-Reader.git

# Subir el código a GitHub
git push -u origin main
```

## 3. Verificar

Una vez que hayas ejecutado los comandos, ve a tu repositorio en GitHub y verifica que todos los archivos estén ahí.

## 4. Opcional: Crear un Release

Para hacer más profesional la distribución:

1. Ve a tu repositorio en GitHub
2. Haz clic en "Releases" → "Create a new release"
3. Tag version: `v1.0.0`
4. Release title: `SHW Reader v1.0.0 - Initial Release`
5. Sube los archivos DMG desde la carpeta `dist/` si quieres distribuir binarios

## URLs que Actualizar

Después de crear el repositorio, actualiza estas URLs en el README.md:

- Reemplaza `yourusername` con tu usuario real de GitHub
- Reemplaza las URLs de Issues y Discussions con las reales

## Estado Actual

✅ Repositorio Git inicializado
✅ Todos los archivos añadidos y committed
✅ README.md profesional creado
✅ Licencia MIT añadida
✅ .gitignore configurado
✅ Proyecto listo para subir

🚀 **El proyecto está 100% listo para subir a GitHub**
