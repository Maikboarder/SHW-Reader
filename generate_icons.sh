#!/bin/bash
# Script para generar iconos multiplataforma para SHW Reader

# Crear directorio para iconos
mkdir -p icons/{macos,windows,android,web}

echo "🎨 SHW Reader - Icon Generator"
echo "Este script generará iconos para todas las plataformas"
echo ""
echo "Requisitos:"
echo "- Imagen source: logo_source.png (recomendado 2048x2048)"
echo "- Fondo transparente"
echo "- sips (macOS) o ImageMagick instalado"
echo ""

# Verificar herramientas disponibles
if command -v sips &> /dev/null; then
    echo "✅ sips encontrado (macOS)"
    TOOL="sips"
elif command -v convert &> /dev/null; then
    echo "✅ ImageMagick encontrado"
    TOOL="convert"
else
    echo "❌ No se encontraron herramientas de procesamiento de imágenes"
    echo "Instala ImageMagick: brew install imagemagick"
    exit 1
fi

echo ""
echo "Tamaños a generar:"
echo "🍎 macOS: 16, 32, 64, 128, 256, 512, 1024"
echo "🪟 Windows: 16, 24, 32, 48, 64, 128, 256"  
echo "🤖 Android: 36, 48, 72, 96, 144, 192"
echo "🌐 Web: 16, 32, 64, 128, 192, 512"
