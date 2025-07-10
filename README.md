# 🎤 SHW Reader - Lector de Archivos Wireless Workbench

Aplicación para leer y editar archivos .shw de Wireless Workbench con dos versiones disponibles: **Escritorio (Tkinter)** y **Web (Flask)**.

## 🚀 Características

### ✨ Funcionalidades Principales
- **Lectura de archivos .shw**: Parser completo de XML para extraer dispositivos y canales
- **Tabla editable**: Edición en vivo de nombres de canales y frecuencias
- **Selección avanzada**: Cmd+Click, Shift+Click y checkboxes para selección múltiple
- **Eliminación selectiva**: Borra solo los canales que desees mantener tu lista limpia
- **Atajos de teclado**: Delete/Backspace para eliminar, Cmd+A/Ctrl+A para seleccionar todo
- **Exportación CSV**: Guarda los datos editados en formato CSV
- **Interfaz moderna**: Diseño limpio y profesional
- **Modo oscuro**: Disponible en la versión web

### 📱 Versión Escritorio (Tkinter)
**Archivo:** `app_selectable.py`

#### Características:
- Interfaz nativa de escritorio
- Edición por doble clic en celdas
- **Selección avanzada**: Cmd+Click (múltiple), Shift+Click (rango)
- **Checkboxes de selección** con "Seleccionar todo"
- **Atajos de teclado**: Delete/Backspace para eliminar, Cmd+A para seleccionar todo
- **Eliminación de filas seleccionadas** con confirmación
- Barras de desplazamiento automáticas
- Exportación directa a CSV
- Compatible con macOS, Windows y Linux

#### Cómo usar:
```bash
python3 app_selectable.py
```

#### Controles:
- **📁 Abrir archivo .shw**: Selecciona y carga un archivo
- **🗑️ Limpiar**: Limpia la tabla actual
- **💾 Exportar CSV**: Guarda los datos en formato CSV
- **🗑️ Eliminar Seleccionados**: Borra las filas marcadas
- **☑️ Checkboxes**: Selecciona filas individuales o todas
- **⌘+Click / Ctrl+Click**: Selección múltiple (agregar/quitar filas)
- **⇧+Click**: Selección de rango (desde la última fila hasta la actual)
- **⌘+A / Ctrl+A**: Seleccionar todas las filas
- **Delete / Backspace**: Eliminar filas seleccionadas
- **Doble clic**: En nombres de canales y frecuencias para editar

### 🌐 Versión Web (Flask)
**Archivos:** `app_web_dark.py` + `templates/index_dark.html`

#### Características:
- **Modo oscuro por defecto** con gradientes modernos
- **Diseño minimalista** y responsive
- **Drag & drop** para cargar archivos
- **Edición en línea** con un clic
- **Selección avanzada**: Cmd+Click (múltiple), Shift+Click (rango)
- **Selección múltiple** con checkboxes estilizados
- **Atajos de teclado**: Delete/Backspace, Cmd+A/Ctrl+A
- **Eliminación selectiva** de canales no deseados
- **Estadísticas en tiempo real**
- **Animaciones suaves** y efectos visuales
- **Compatible móvil**

#### Cómo usar:
```bash
# Instalar dependencias (si no están instaladas)
pip3 install flask

# Ejecutar la aplicación
python3 app_web_dark.py
```

Luego abre: `http://localhost:5000`

#### Controles Web:
- **Drag & Drop**: Arrastra archivos .shw directamente a la ventana
- **📁 Seleccionar archivo**: Botón de carga tradicional
- **☑️ Selección múltiple**: Checkboxes individuales y "Seleccionar todo"
- **⌘+Click / Ctrl+Click**: Selección múltiple (toggle individual)
- **⇧+Click**: Selección de rango (desde la última fila seleccionada)
- **⌘+A / Ctrl+A**: Seleccionar todas las filas
- **Delete / Backspace**: Eliminar filas seleccionadas
- **Clic simple**: En nombres de canales y frecuencias para editar
- **Enter**: Guarda la edición
- **Escape**: Cancela la edición
- **💾 Exportar CSV**: Descarga automática
- **🗑️ Eliminar Seleccionados**: Borra solo las filas marcadas
- **🧹 Limpiar tabla**: Borra todos los datos

## 📊 Formato de Datos

La aplicación extrae los siguientes campos de archivos .shw:

| Campo | Descripción | Editable |
|-------|-------------|----------|
| **Dispositivo/Modelo** | Nombre del dispositivo y modelo | ❌ |
| **Nombre del Canal** | Nombre asignado al canal | ✅ |
| **Frecuencia** | Frecuencia en MHz | ✅ |
| **RF Zone** | Zona de RF configurada | ❌ |
| **Banda** | Banda de frecuencia | ❌ |

## 🎯 Selección y Eliminación de Canales

### ¿Por qué es útil?
Cuando trabajas con archivos .shw grandes, es común que tengas canales que no necesitas o que quieras eliminar para limpiar tu lista. Esta funcionalidad te permite:

- **Seleccionar canales específicos** que quieres eliminar
- **Mantener solo los canales relevantes** para tu proyecto
- **Limpiar listas grandes** de manera eficiente
- **Preservar la configuración** de los canales que sí necesitas

### Cómo usar la selección:

#### 🖱️ Métodos de Selección:

**Selección Simple:**
- **Clic normal**: Selecciona una sola fila (deselecciona las demás)
- **Checkbox individual**: Marca/desmarca una fila específica

**Selección Múltiple:**
- **⌘+Clic** (Mac) / **Ctrl+Clic** (Windows/Linux): Agrega o quita filas de la selección
- **⇧+Clic**: Selecciona un rango desde la última fila seleccionada hasta la actual
- **⌘+A** (Mac) / **Ctrl+A** (Windows/Linux): Selecciona todas las filas

**Eliminación:**
- **Delete** o **Backspace**: Elimina las filas seleccionadas
- **Botón "Eliminar Seleccionados"**: Alternativa visual para eliminar

#### Versión Escritorio:
1. ☑️ **Checkbox individual**: Marca cada fila que quieres eliminar
2. ☑️ **Seleccionar todo**: Usa el checkbox del encabezado para seleccionar/deseleccionar todas las filas
3. 🖱️ **Selección avanzada**: Cmd+Click para múltiple, Shift+Click para rangos
4. ⌨️ **Atajos de teclado**: Delete para eliminar, Cmd+A para seleccionar todo
5. 🗑️ **Eliminar seleccionados**: Confirma la eliminación de las filas marcadas
6. 👁️ **Feedback visual**: Las filas seleccionadas se resaltan en azul

#### Versión Web:
1. ☑️ **Checkboxes estilizados**: Selección visual moderna con efectos hover
2. 🎛️ **Estado indeterminado**: El checkbox principal muestra estados parciales
3. 🖱️ **Clics avanzados**: Cmd+Click y Shift+Click con feedback visual inmediato
4. ⚡ **Eliminación inmediata**: Sin recarga de página
5. 📊 **Contador en tiempo real**: Ve cuántas filas has seleccionado

## 🎨 Diseño Visual

### Versión Web - Modo Oscuro
- **Colores principales**: Gradientes oscuros (#1a1a1a → #0f0f0f)
- **Acentos**: Azul moderno (#64b5f6) y verde (#81c784)
- **Tipografía**: Segoe UI con pesos ligeros
- **Efectos**: Sombras suaves, hover animations, gradientes en botones
- **Responsive**: Adaptable a móviles y tablets

### Versión Escritorio
- **Colores**: Grises suaves con acentos azules
- **Tabla**: Filas alternadas con separadores visuales
- **Iconos**: Emojis para mejor UX
- **Layout**: Distribución clásica de escritorio

## 🔧 Estructura del Proyecto

```
/
├── app_selectable.py              # Versión Tkinter con selección (escritorio)
├── app_web_dark.py               # Versión Flask (web oscura)
├── templates/
│   └── index_dark.html           # Template web con modo oscuro
├── uploads/                      # Carpeta temporal para archivos
└── README.md                     # Esta documentación
```

## 🐛 Solución de Problemas

### Versión Tkinter
- **macOS**: Las advertencias de deprecation están silenciadas automáticamente
- **Errores de anchor**: Corregidos en la versión actual
- **Scroll**: Funciona con rueda del ratón y barras

### Versión Web
- **Puerto ocupado**: Cambia el puerto en `app.run(port=5001)`
- **Flask no instalado**: `pip3 install flask`
- **Archivos grandes**: Límite de 16MB configurado

## 📈 Próximas Mejoras

- [ ] **Validación de frecuencias**: Verificar rangos válidos
- [ ] **Filtros avanzados**: Por banda, zona, dispositivo
- [ ] **Ordenamiento**: Columnas ordenables
- [ ] **Búsqueda**: Filtro de texto en tiempo real
- [x] **Selección múltiple**: ✅ Implementado - Checkboxes, Cmd+Click, Shift+Click, Delete
- [x] **Atajos de teclado**: ✅ Implementado - Delete, Backspace, Cmd+A, Ctrl+A
- [x] **Aplicación nativa macOS**: ✅ Implementado - App nativa con Electron
- [ ] **Duplicación de canales**: Copiar configuraciones similares
- [ ] **Temas**: Modo claro para la versión web
- [ ] **Base de datos**: Persistencia de datos editados
- [ ] **Multi-archivo**: Cargar múltiples .shw simultáneamente
- [ ] **Exportar a .shw**: Generar archivos Wireless Workbench editados

## 🎯 Recomendación de Uso

### Para uso casual/personal:
**Versión Web** - Más moderna, fácil de usar, mejor experiencia visual

### Para uso profesional/empresarial:
**Aplicación nativa macOS** - Instalación sencilla, funcionamiento offline, experiencia completa

### Para desarrollo/testing:
**Versión Escritorio** - Más rápida para desarrollo, no requiere servidor web

## 📦 Aplicación Nativa macOS (COMPLETADA)

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

**Desarrollado con ❤️ para técnicos de audio profesional**
