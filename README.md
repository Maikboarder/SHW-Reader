
# SHW Reader - Lector de Archivos Wireless Workbench

Aplicación para visualizar y editar archivos .shw de Wireless Workbench. Disponible en versión de escritorio y web.


## Características principales
- Lectura de archivos .shw
- Edición de nombres de canales y frecuencias
- Selección múltiple avanzada (Cmd/Ctrl+Click, Shift+Click, checkboxes)
- Eliminación selectiva de canales
- Atajos de teclado para selección y borrado
- Exportación a CSV y PDF


### Versión Escritorio
**Archivo principal:** `app_selectable.py`

Características:
- Interfaz nativa multiplataforma
- Edición directa en tabla
- Selección múltiple y atajos de teclado
- Exportación a CSV

Uso rápido:
```bash
python3 app_selectable.py
```


### Versión Web (Flask)
**Archivos principales:** `app_web_dark.py`, `templates/index_dark.html`

Características:
- Modo oscuro y diseño responsive
- Drag & drop para cargar archivos
- Edición y selección múltiple en línea
- Exportación a CSV

Uso rápido:
```bash
pip3 install flask
python3 app_web_dark.py
```
Abre: http://localhost:5000



# SHW Reader v1.0.2

**SHW Reader** es una aplicación de escritorio para visualizar y exportar datos de archivos Wireless Workbench (.shw) de Shure.

## Instalación

1. Descarga el instalador para tu sistema operativo desde la sección de releases.
2. Instala la aplicación siguiendo el asistente.
3. Abre SHW Reader y comienza a importar tus archivos .shw.

## Uso básico

1. Haz clic en “Importar archivo” y selecciona un archivo .shw.
2. Visualiza la tabla de dispositivos y canales.
3. Exporta los datos a CSV si lo necesitas.

## Requisitos

- macOS 10.15+ (Apple Silicon y Intel)
- No requiere Python ni dependencias externas

## Licencia

Este proyecto está bajo la licencia MIT.
- **Checkbox individual**: Marca/desmarca una fila específica

**Selección Múltiple:**
- **⌘+Clic** (Mac) / **Ctrl+Clic** (Windows/Linux): Agrega o quita filas de la selección
- **⇧+Clic**: Selecciona un rango desde la última fila seleccionada hasta la actual
- **⌘+A** (Mac) / **Ctrl+A** (Windows/Linux): Selecciona todas las filas

**Eliminación:**
- **Delete** o **Backspace**: Elimina las filas seleccionadas
- **Botón "Eliminar Seleccionados"**: Alternativa visual para eliminar


# SHW Reader v1.0.2

**SHW Reader** es una aplicación de escritorio para visualizar y exportar datos de archivos Wireless Workbench (.shw) de Shure.

## Instalación

1. Descarga el instalador para macOS desde la sección de releases.
2. Instala la aplicación siguiendo el asistente.
3. Abre SHW Reader y comienza a importar tus archivos .shw.

## Uso básico

1. Haz clic en “Importar archivo” y selecciona un archivo .shw.
2. Visualiza la tabla de dispositivos y canales.
3. Exporta los datos a CSV si lo necesitas.

## Requisitos

- macOS 10.15+ (Apple Silicon)
- No requiere Python ni dependencias externas

## Licencia

MIT

## Recomendación de uso

### Para uso casual/personal:
**Versión Web** - Más moderna, fácil de usar, mejor experiencia visual

### Para uso profesional/empresarial:
**Aplicación nativa macOS** - Instalación sencilla, funcionamiento offline, experiencia completa

### Para desarrollo/testing:
**Versión Escritorio** - Más rápida para desarrollo, no requiere servidor web


## Aplicación nativa macOS

### ✅ **Aplicación lista para usar**

Se ha creado exitosamente una aplicación nativa de macOS que combina la experiencia web moderna con la comodidad de una app nativa.

#### 📁 Archivos disponibles en `dist/`:
- **`SHW Reader-1.0.0.dmg`** - Instalador para Mac Intel (x64)
- **`SHW Reader-1.0.0-arm64.dmg`** - Instalador para Mac Apple Silicon (M1/M2/M3)
- **`SHW Reader-1.0.0-mac.zip`** - App empaquetada para Mac Intel
- **`SHW Reader-1.0.0-arm64-mac.zip`** - App empaquetada para Mac Apple Silicon

#### 🚀 **Instalación**:
1. Descarga el `.dmg` apropiado para tu Mac
2. Abre el archivo `.dmg`
3. Arrastra `SHW Reader.app` a la carpeta `Applications`
4. Ejecuta desde Launchpad o Finder

#### ✨ **Características de la app nativa**:
- ✅ **Instalación estándar** (como cualquier app de macOS)
- ✅ **Icono personalizado** con diseño de audio profesional
- ✅ **Lanzamiento desde Launchpad**
- ✅ **Funcionamiento offline** (no requiere conexión a internet)
- ✅ **Modo oscuro nativo**
- ✅ **Ventana optimizada** (1400x900px)
- ✅ **Gestión automática** del servidor Flask interno
- ✅ **Compatible** con macOS 10.15+ (Catalina y posteriores)
- ✅ **Arquitecturas duales** (Intel y Apple Silicon)

#### ⚙️ **Reconstruir la aplicación** (para desarrolladores):
```bash
# 1. Instalar dependencias
npm install

# 2. Reconstruir iconos (opcional)
python3 create_icons.py

# 3. Compilar aplicación nativa
npm run build
```

---


Desarrollado para técnicos de audio profesional y usuarios que buscan eficiencia y claridad.
