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
  
  **⬇️ Ready to use? Jump to [Quick Download](#-quick-start)**
</div>

## 🎯 **What is SHW Reader?**

SHW Reader is a **free, professional tool** for audio engineers and technicians who work with **Shure Wireless Workbench** files. It lets you:

- 📖 **View SHW files** in a clean, modern interface
- ✏️ **Edit channel names and frequencies** directly
- 📊 **Export to multiple formats**: CSV, Excel, Word, PDF
- 🌍 **Use in your language**: 9 languages supported
- 🎨 **Choose your theme**: Dark or light mode

**Perfect for:** Live sound engineers, system integrators, audio consultants, and anyone working with wireless microphone coordination.

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

### 📥 **Direct Downloads** (Recommended for most users)

<div align="center">

**🍎 Choose your Mac type:**

[![Download for Apple Silicon](https://img.shields.io/badge/Download%20for%20Apple%20Silicon-M1%2C%20M2%2C%20M3%20Macs-blue?style=for-the-badge&logo=apple)](https://github.com/Maikboarder/SHW-Reader/releases/latest/download/SHW-Reader-macOS-arm64.dmg)

[![Download for Intel Macs](https://img.shields.io/badge/Download%20for%20Intel%20Macs-Intel%20Processor-lightgrey?style=for-the-badge&logo=intel)](https://github.com/Maikboarder/SHW-Reader/releases/latest/download/SHW-Reader-macOS-x64.dmg)

**❓ Not sure which Mac you have?**
- **Apple Silicon** (M1, M2, M3): Most Macs from 2021 onwards
- **Intel**: Most Macs from 2020 and earlier
- Check: Apple Menu → About This Mac

</div>

### Prerequisites
- macOS 10.14 or later
- Python 3.8 or later

### Installation

1. **Download the DMG** using the buttons above
2. **Open the downloaded DMG file**
3. **Drag SHW Reader to Applications folder**
4. **Launch** SHW Reader from Applications
5. **Allow permissions** if macOS asks (it's safe!)

### Alternative: GitHub Releases

1. **Browse all releases** at [Releases](https://github.com/Maikboarder/SHW-Reader/releases) page
2. **Download the appropriate file**:
   - For Apple Silicon Macs: `SHW-Reader-macOS-arm64.dmg`
   - For Intel Macs: `SHW-Reader-macOS-x64.dmg`

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

### 📞 **Need Help?**

- **📧 Email Support**: [maikboarder@gmail.com](mailto:maikboarder@gmail.com)
- **🐞 Bug Reports**: [GitHub Issues](https://github.com/Maikboarder/SHW-Reader/issues)
- **💡 Feature Requests**: [GitHub Discussions](https://github.com/Maikboarder/SHW-Reader/discussions)

### 🆘 **Common Issues**

**Q: "SHW Reader can't be opened because it's from an unidentified developer"**
- **Solution**: Right-click the app → Open → Open anyway

**Q: "Python not found" error**
- **Solution**: Install Python from [python.org](https://www.python.org/downloads/macos/)

**Q: "Which version should I download?"**
- **M1/M2/M3 Mac**: Download Apple Silicon version
- **Intel Mac**: Download Intel version
- **Check**: Apple Menu → About This Mac

**Q: App won't start or crashes**
- **Solution**: Try the other version (Intel/Silicon) or contact support

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
