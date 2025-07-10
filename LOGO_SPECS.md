# Logo Professional Specifications for SHW Reader

## Platform Requirements

### macOS (.icns format)
- 16x16, 32x32, 64x64, 128x128, 256x256, 512x512, 1024x1024
- Retina: 32x32@2x, 64x64@2x, 128x128@2x, 256x256@2x, 512x512@2x

### Windows (.ico format)  
- 16x16, 24x24, 32x32, 48x48, 64x64, 128x128, 256x256

### Android (Adaptive Icons)
- 108x108 (foreground layer)
- 108x108 (background layer) 
- 72x72 (legacy)
- Multiple densities: mdpi, hdpi, xhdpi, xxhdpi, xxxhdpi

### Web/App Icons
- 16x16 (favicon)
- 32x32 (small icon)
- 64x64 (medium icon)
- 128x128 (large icon)
- 192x192 (Android Chrome)
- 512x512 (iOS/PWA)

## Design Guidelines

### Visual Requirements
- **Transparent background**
- **Clear silhouette** at small sizes (16x16)
- **High contrast** for light/dark themes
- **Simple, recognizable shape**
- **Consistent visual weight**

### Technical Requirements
- **Vector source** (SVG/AI/Sketch)
- **PNG exports** with alpha channel
- **Consistent padding** (10-15% margin)
- **Sharp edges** at pixel boundaries
- **Optimized file size**

## Current Status
- ✅ Base PNG available (1024x1024)
- ✅ Transparent background implemented
- ✅ Multiple sizes generated (16x16 to 512x512@2x)
- ✅ macOS .icns format ready
- ✅ Professional iconset structure
- ✅ Integrated in Electron app
- ✅ Web favicons implemented
- ✅ Retina displays supported

## Next Steps
1. ✅ Create transparent background version
2. ✅ Generate multiple sizes  
3. ✅ Create platform-specific formats
4. ✅ Integrate in application
5. 🔄 Test on all target platforms
6. 📱 Create Android adaptive icons (future)
7. 🪟 Create Windows .ico format (future)
