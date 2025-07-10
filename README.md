# SHW Reader

<div align="center">
  <img src="assets/SHW Reader.png" alt="SHW Reader Logo" width="128">
  
  **Professional SHW File Viewer and Export Tool**
  
  *A multi-language Electron application for viewing and exporting Wireless Workbench SHW files*
  
  **Created by Miguel Fuentes Rodriguez ([@Maikboarder](https://github.com/Maikboarder))**
  
  [![GitHub release](https://img.shields.io/github/release/Maikboarder/SHW-Reader.svg)](https://github.com/Maikboarder/SHW-Reader/releases)
  [![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
  [![macOS](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://github.com/Maikboarder/SHW-Reader)
  
  **💖 Support the Project**
  
  [![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Support%20Development-orange?style=for-the-badge&logo=buy-me-a-coffee)](https://buymeacoffee.com/maikboarder)
  
  *If SHW Reader helps your workflow, consider supporting its development!*
</div>

## 🌟 Features

- **📁 SHW File Support**: Native viewer for Wireless Workbench SHW files
- **🌍 Multi-language**: Support for 9 languages (Spanish, English, French, German, Italian, Portuguese, Catalan, Galician, Basque)
- **📊 Export Options**: Export to CSV, Excel, Word, and PDF formats
- **🎨 Modern UI**: Dark/Light theme support with professional design
- **🖥️ Native macOS**: Optimized for macOS with native UI elements
- **⚡ Fast Performance**: Built with Electron and Flask for optimal performance
- **✏️ Editable Tables**: Edit channel names and frequencies in real-time
- **🔍 Advanced Selection**: Multiple selection modes with keyboard shortcuts

## 🚀 Quick Start

### Prerequisites
- macOS 10.14 or later
- Python 3.8 or later

### Installation

1. **Download the latest release** from the [Releases](https://github.com/Maikboarder/SHW-Reader/releases) page
2. **Install the app**:
   - For Apple Silicon Macs: Download `SHW-Reader-macOS-arm64.dmg`
   - For Intel Macs: Download `SHW-Reader-macOS-x64.dmg`
3. **Open the DMG** and drag SHW Reader to Applications
4. **Launch** SHW Reader from Applications

### Development Setup

```bash
# Clone the repository
git clone https://github.com/Maikboarder/SHW-Reader.git
cd SHW-Reader

# Install dependencies
npm install
pip3 install -r requirements.txt

# Run in development mode
npm start
```

## 📖 Usage

1. **Open a SHW file**: File → Open File (⌘O) or drag & drop
2. **View data**: Browse frequency coordination data in the table
3. **Edit data**: Double-click cells to edit channel names and frequencies
4. **Select rows**: Use checkboxes, Cmd+Click for multiple, Shift+Click for range
5. **Export data**: Choose format from Export menu or dropdown
6. **Change language**: Use Language menu or UI selector
7. **Switch themes**: View → Theme → Dark/Light Mode

## 🛠️ Building from Source

### Build for macOS

```bash
# Build for current architecture
npm run build:mac

# Build for specific architecture
npm run build:mac-intel    # Intel Macs
npm run build:mac-silicon  # Apple Silicon
npm run build:mac-universal # Universal binary
```

See [BUILD_GUIDE.md](BUILD_GUIDE.md) for detailed building instructions.

## 🌐 Supported Languages

- **🇪🇸 Español** (Spanish)
- **🇺🇸 English**
- **🇫🇷 Français** (French)
- **🇩🇪 Deutsch** (German)
- **🇮🇹 Italiano** (Italian)
- **🇵🇹 Português** (Portuguese)
- **🇪🇸 Català** (Catalan)
- **🇪🇸 Galego** (Galician)
- **🇪🇸 Euskera** (Basque)

## 📋 Export Formats

| Format | Description | Use Case |
|--------|-------------|----------|
| **CSV** | Comma-separated values | Data analysis, spreadsheets |
| **Excel** | Microsoft Excel format | Professional reports |
| **Word** | Microsoft Word document | Documentation, presentations |
| **PDF** | Portable Document Format | Sharing, archiving |

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `⌘O` | Open SHW file |
| `⌘E` | Export to CSV |
| `⌘⇧E` | Export to Excel |
| `⌘⇧W` | Export to Word |
| `⌘⇧P` | Export to PDF |
| `⌘A` | Select all rows |
| `⌘K` | Clear table |
| `Delete` | Delete selected rows |
| `F12` | Toggle Developer Tools |
| `⌘R` | Reload application |

## 🔧 Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Python 3.8+ with Flask
- **Desktop**: Electron 31+
- **Build**: electron-builder
- **Packaging**: DMG for macOS distribution
- **Export Libraries**: openpyxl (Excel), python-docx (Word), reportlab (PDF)

## 📁 Project Structure

```
SHW-Reader/
├── electron-main.js      # Electron main process
├── app_desktop.py        # Flask backend server
├── templates/            # HTML templates
├── static/              # CSS, images, assets
├── translations/        # Multi-language support
├── assets/             # Icons and build assets
├── dist/               # Build output
├── build-macos.sh      # Build script
├── BUILD_GUIDE.md      # Build instructions
└── package.json        # Project configuration
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## � Support the Project

If SHW Reader has been useful for your audio work, consider supporting its development:

<div align="center">
  <a href="https://buymeacoffee.com/maikboarder">
    <img src="https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Support%20Development-orange?style=for-the-badge&logo=buy-me-a-coffee" alt="Buy Me A Coffee">
  </a>
</div>

Your support helps maintain and improve SHW Reader for the entire audio community! 🎵

## �📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Issues & Support

- **Bug Reports**: [GitHub Issues](https://github.com/Maikboarder/SHW-Reader/issues)
- **Feature Requests**: [GitHub Discussions](https://github.com/Maikboarder/SHW-Reader/discussions)

---

<div align="center">
  <strong>SHW Reader v1.0.0</strong><br>
  Created with ❤️ by <strong>Miguel Fuentes Rodriguez</strong><br>
  <em>For the audio professional community</em>
  
  <br><br>
  
  **👨‍💻 Developer**<br>
  [Miguel Fuentes Rodriguez](https://github.com/Maikboarder) ([@Maikboarder](https://github.com/Maikboarder))<br>
  <em>Audio Professional & Software Developer</em>
  
  <br>
  
  **💖 Support Miguel's Work**<br>
  [![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Support%20Miguel-orange?style=flat-square&logo=buy-me-a-coffee)](https://buymeacoffee.com/maikboarder)
</div>
