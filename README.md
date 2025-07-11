# SHW Reader

<div align="center">
  <img src="assets/SHW Reader.png" alt="SHW Reader Logo" width="128">
  
  **Professional SHW File Viewer and Export Tool**
  
  *A multi-language Electron application for viewing and exporting Wireless Workbench SHW files*
  
  **Especialmente dirigida a Coordinadores de RF, ingenieros de sonido y técnicos que gestionan espectro inalámbrico profesional.**
  
  **Created by Miguel Fuentes Rodriguez ([@Maikboarder](https://github.com/Maikboarder))**
  
  [![GitHub release](https://img.shields.io/github/release/Maikboarder/SHW-Reader.svg)](https://github.com/Maikboarder/SHW-Reader/releases)
  [![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
  [![macOS](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://github.com/Maikboarder/SHW-Reader)
  [![Windows](https://img.shields.io/badge/platform-Windows-blue.svg)](https://github.com/Maikboarder/SHW-Reader)
  
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

- **� Zero Dependencies**: Built-in Python server - no need to install Python separately
- **�📁 SHW File Support**: Native viewer for Wireless Workbench SHW files
- **🌍 Multi-language**: Support for 9 languages (Spanish, English, French, German, Italian, Portuguese, Catalan, Galician, Basque)
- **📊 Export Options**: Export to CSV, Excel, Word, and PDF formats
- **🎨 Modern UI**: Dark/Light theme support with professional design
- **🖥️ Cross-platform**: Optimized for macOS and Windows with native UI elements
- **⚡ Fast Performance**: Built with Electron and embedded Flask server for optimal performance
- **✏️ Editable Tables**: Edit channel names and frequencies in real-time
- **🔍 Advanced Selection**: Multiple selection modes with keyboard shortcuts
- **🛡️ Robust Fallbacks**: Intelligent server detection with multiple backup options

## 🚀 Quick Start

### 📥 **Direct Downloads** (Recommended for most users)

> **🎉 NEW v1.0.0**: Now with **embedded backend** - no Python installation required!

<div align="center">

**🍎 macOS Downloads:**

[![Download for Apple Silicon](https://img.shields.io/badge/Download%20for%20Apple%20Silicon-M1%2C%20M2%2C%20M3%20Macs-blue?style=for-the-badge&logo=apple)](https://github.com/Maikboarder/SHW-Reader/releases/download/v1.0.0/SHW%20Reader-1.0.0-arm64.dmg)

[![Download for Intel Macs](https://img.shields.io/badge/Download%20for%20Intel%20Macs-Intel%20Processor-lightgrey?style=for-the-badge&logo=intel)](https://github.com/Maikboarder/SHW-Reader/releases/download/v1.0.0/SHW%20Reader-1.0.0.dmg)

**🪟 Windows Downloads:**

[![Download Windows Installer](https://img.shields.io/badge/Download%20Windows%20Installer-Setup%20.exe-blue?style=for-the-badge&logo=windows)](https://github.com/Maikboarder/SHW-Reader/releases/download/v1.0.0/SHW%20Reader%20Setup%201.0.0.exe)

[![Download Windows Portable](https://img.shields.io/badge/Download%20Windows%20Portable-Portable%20.exe-green?style=for-the-badge&logo=windows)](https://github.com/Maikboarder/SHW-Reader/releases/download/v1.0.0/SHW%20Reader%201.0.0.exe)

**❓ Which version to choose?**
- **macOS**: Apple Silicon (M1/M2/M3) or Intel based on your Mac
- **Windows**: Installer for system-wide installation, Portable for no-install usage

**🔗 All Releases**: [View all versions and download options](https://github.com/Maikboarder/SHW-Reader/releases)

</div>

### ✅ **System Requirements**
- **macOS**: macOS 10.14 or later
- **Windows**: Windows 10 or later
- **🚀 No Python installation required** - Built-in server included!

> **Note**: SHW Reader now includes an embedded Python server, so you don't need to install Python separately. The application will work immediately after download and installation.

**🔧 Having installation issues?** Check our [Troubleshooting Guide](TROUBLESHOOTING.md) for solutions to common Python installation problems.

### Installation

#### macOS
1. **Download the DMG** using the buttons above
2. **Open the downloaded DMG file**
3. **Drag SHW Reader to Applications folder**
4. **Launch** SHW Reader from Applications
5. **Allow permissions** if macOS asks (it's safe!)

#### Windows
1. **Download the installer or portable version** using the buttons above
2. **For Installer**: Run the downloaded `.exe` and follow setup wizard
3. **For Portable**: Extract and run the `.exe` directly (no installation needed)
4. **Allow Windows Defender** if it asks (it's safe!)

**⚠️ Important for Windows Users:**
- If you see "Error installing Python", SHW Reader will run in **Basic Mode** with limited functionality
- For full features, install Python manually from [python.org](https://python.org/downloads/) 
- During Python installation, check "Add Python to PATH"
- See our [Troubleshooting Guide](TROUBLESHOOTING.md) for detailed help

### Alternative: GitHub Releases

1. **Browse all releases** at [Releases](https://github.com/Maikboarder/SHW-Reader/releases) page
2. **Download the appropriate file**:
   - **macOS Apple Silicon**: `SHW Reader-1.0.0-arm64.dmg`
   - **macOS Intel**: `SHW Reader-1.0.0.dmg`
   - **Windows Installer**: `SHW Reader Setup 1.0.0.exe`
   - **Windows Portable**: `SHW Reader 1.0.0.exe`

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

### Build for macOS and Windows

```bash
# Build for macOS current architecture
npm run build:mac

# Build for specific macOS architecture
npm run build:mac-intel    # Intel Macs
npm run build:mac-silicon  # Apple Silicon
npm run build:mac-universal # Universal binary

# Build for Windows
npm run build:win          # All Windows targets
npm run build:win-x64      # Windows 64-bit
npm run build:win-ia32     # Windows 32-bit
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
- **macOS**: M1/M2/M3 Mac → Apple Silicon version, Intel Mac → Intel version
- **Windows**: Most users → Windows Installer, Advanced users → Portable version
- **Check macOS type**: Apple Menu → About This Mac

**Q: App won't start or crashes**
- **macOS**: Try the other version (Intel/Silicon) or contact support
- **Windows**: Run as administrator, or try compatibility mode for Windows 10

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
