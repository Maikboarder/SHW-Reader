# SHW Reader

[![GitHub release](https://img.shields.io/github/release/Maikboarder/SHW-Reader.svg)](https://github.com/Maikboarder/SHW-Reader/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![macOS](https://img.shields.io/badge/platform-macOS%20Silicon-blue?logo=apple)](https://github.com/Maikboarder/SHW-Reader/releases)

<div align="center">
  <a href="https://buymeacoffee.com/maikboarder"><img src="https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Support%20Development-orange?style=for-the-badge&logo=buy-me-a-coffee" alt="Buy Me A Coffee"></a>
  <a href="https://github.com/sponsors/Maikboarder"><img src="https://img.shields.io/badge/GitHub%20Sponsors-Become%20a%20Sponsor-pink?style=for-the-badge&logo=github-sponsors" alt="GitHub Sponsors"></a>
</div>

---

## ⚠️ Importante para usuarios de macOS

**SHW Reader NO está firmada ni notarizada por Apple.**

- En las versiones recientes de macOS, Gatekeeper puede bloquear la app descargada (tanto en .dmg como en .zip) mostrando el mensaje:
  > “El archivo está dañado y debe trasladarse a la papelera”
- Esto ocurre porque la app contiene binarios embebidos y no está firmada con un Apple Developer ID.
- No hay forma de evitar este mensaje para todos los usuarios sin pagar a Apple y firmar/notarizar la app.
- Incluso usando .zip, macOS puede bloquear la app.

### ¿Qué puedes hacer?
- Si eres usuario avanzado, puedes intentar quitar la cuarentena tras descomprimir/copiar la app:
  ```sh
  xattr -dr com.apple.quarantine "/ruta/a/SHW Reader.app"
  ```
- Si el sistema sigue bloqueando la app, **no hay solución universal sin firma y notarización**.
- Para uso personal, puedes desactivar temporalmente Gatekeeper (no recomendado):
  ```sh
  sudo spctl --master-disable
  ```
- Para distribución pública, es imprescindible firmar y notarizar la app.

---

## 🛠️ Cómo compilar SHW Reader en macOS

1. Clona el repositorio:
   ```sh
   git clone https://github.com/Maikboarder/SHW-Reader.git
   cd SHW-Reader
   ```
2. Instala dependencias:
   ```sh
   npm install
   pip3 install -r requirements.txt
   ```
3. Genera el ejecutable backend:
   ```sh
   npm run build:mac-silicon
   ```
   El instalador .dmg y la app estarán en la carpeta `dist/`.
4. (Opcional) Comprime la app en .zip para compartir:
   ```sh
   cd dist/mac-arm64
   zip -r "SHW Reader-1.0.2-arm64.zip" "SHW Reader.app"
   ```

---

**SHW Reader** es una aplicación de escritorio para visualizar y exportar datos de archivos Wireless Workbench (.shw) de Shure.

- Exportación a CSV y PDF
- Soporte para macOS 10.15+ (Apple Silicon)
- Idiomas disponibles: Español, Inglés, Francés, Alemán, Italiano, Portugués, Catalán, Gallego, Euskera

### 🚀 Descargar

[⬇️ Descargar para Mac Silicon (M1/M2/M3)](https://github.com/Maikboarder/SHW-Reader/releases/latest)

> Próximamente: versiones para Windows y Mac Intel

### ☕️ ¡Apoya el proyecto!

Si SHW Reader te resulta útil, puedes ayudar a su desarrollo:
- [Invítame a un café](https://buymeacoffee.com/maikboarder)
- [GitHub Sponsors](https://github.com/sponsors/Maikboarder)

### Instalación
1. Descarga el instalador desde el enlace anterior.
2. Abre el archivo `.dmg` y arrastra SHW Reader a `Aplicaciones`.
3. Ejecuta la app y comienza a importar tus archivos .shw.

### Uso básico
1. Haz clic en “Importar archivo” y selecciona un archivo .shw.
2. Visualiza la tabla de dispositivos y canales.
3. Exporta los datos a CSV o PDF si lo necesitas.

---

**SHW Reader** is a desktop app to view and export Shure Wireless Workbench (.shw) files.

- Export to CSV and PDF
- Supports macOS 10.15+ (Apple Silicon)
- Available languages: Spanish, English, French, German, Italian, Portuguese, Catalan, Galician, Basque

### 🚀 Download

[⬇️ Download for Mac Silicon (M1/M2/M3)](https://github.com/Maikboarder/SHW-Reader/releases/latest)

> Coming soon: Windows and Mac Intel versions

### ☕️ Support the project!

If SHW Reader is useful for you, please consider supporting development:
- [Buy Me a Coffee](https://buymeacoffee.com/maikboarder)
- [GitHub Sponsors](https://github.com/sponsors/Maikboarder)

### Installation
1. Download the installer from the link above.
2. Open the `.dmg` file and drag SHW Reader to `Applications`.
3. Launch the app and start importing your .shw files.

### Basic usage
1. Click “Import file” and select a .shw file.
2. View the device and channel table.
3. Export data to CSV or PDF if needed.

---

## Licencia / License

MIT

---

**Desarrollado por Miguel Fuentes Rodriguez ([Maikboarder](https://github.com/Maikboarder))**
