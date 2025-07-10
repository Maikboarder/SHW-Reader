# Sistema de Multilenguaje - SHW Reader

## Idiomas Soportados

La aplicación SHW Reader ahora soporta múltiples idiomas:

1. **🇪🇸 Español** (por defecto)
2. **🇺🇸 English**
3. **🇫🇷 Français**
4. **🇩🇪 Deutsch**
5. **🇮🇹 Italiano**
6. **🇵🇹 Português**
7. **🏴 Català**
8. **🏴 Galego**
9. **🏴 Euskera**

## Arquitectura del Sistema

### Backend (Flask)
- **Rutas API**:
  - `/api/languages` - Obtiene idiomas disponibles
  - `/api/translations/<lang>` - Obtiene traducciones para un idioma específico
  - `/api/set_language` - Establece idioma preferido del usuario

- **Archivos de traducción**: `translations/`
  - `config.json` - Configuración de idiomas
  - `es.json`, `en.json`, `fr.json`, etc. - Archivos de traducción por idioma

### Frontend (JavaScript)
- **Sistema de traducción dinámico**:
  - Carga automática de traducciones al inicializar
  - Selector de idioma en la interfaz
  - Aplicación automática de traducciones usando `data-i18n`
  - Persistencia de idioma en localStorage

### Menú de Electron
- **Menú "Idioma"** con todos los idiomas disponibles
- Cambio de idioma sin recargar la página
- Sincronización con selector de la interfaz web

## Uso

### Cambiar Idioma desde la Interfaz
1. Usar el selector de idioma en la esquina superior derecha
2. Los cambios se aplican inmediatamente sin recargar

### Cambiar Idioma desde el Menú
1. Menú → Idioma → Seleccionar idioma deseado
2. Los cambios se aplican inmediatamente

### Persistencia
- El idioma seleccionado se guarda automáticamente
- Se restaura al reiniciar la aplicación

## Elementos Traducidos

- **Interfaz principal**:
  - Títulos y encabezados
  - Etiquetas de columnas de la tabla
  - Botones y controles
  - Mensajes de estado
  - Menús contextuales

- **Mensajes del sistema**:
  - Confirmaciones
  - Errores
  - Estados de carga
  - Notificaciones

- **Exportación**:
  - Encabezados de CSV respetan el idioma seleccionado

## Estructura de Archivos de Traducción

```json
{
  "app_title": "Título de la aplicación",
  "table_headers": {
    "channel": "Nombre del Canal",
    "frequency": "Frecuencia",
    ...
  },
  "messages": {
    "file_uploaded": "Archivo cargado...",
    "confirm_delete": "¿Confirmar eliminación de {count} elemento(s)?",
    ...
  }
}
```

### Placeholders
- Se soportan placeholders con `{variable}`
- Ejemplo: `"rows_deleted": "{count} filas eliminadas"`

## Agregar Nuevos Idiomas

1. Crear archivo `translations/nuevo_idioma.json`
2. Agregar entrada en `translations/config.json`
3. Actualizar menú de Electron en `electron-main.js`
4. El sistema detectará automáticamente el nuevo idioma

## Fallbacks
- Si una traducción no existe, se usa inglés como fallback
- Si inglés no existe, se usa español
- Si nada existe, se muestra la clave de traducción

## Mejoras Implementadas

✅ **Sistema completo de traducciones**
✅ **Interfaz de selector de idioma**
✅ **Menú de Electron multilenguaje**
✅ **Persistencia de preferencias**
✅ **API REST para traducciones**
✅ **Soporte para 9 idiomas**
✅ **Traducción dinámica sin recargas**
✅ **Exportación CSV multilenguaje**
✅ **Fallbacks robustos**

La aplicación mantiene toda su funcionalidad previa mientras añade un soporte completo para múltiples idiomas, mejorando significativamente la experiencia del usuario a nivel internacional.
