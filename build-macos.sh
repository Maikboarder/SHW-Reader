#!/bin/bash

# Script de compilación para SHW Reader en macOS
# Este script compila la aplicación para Intel (x64) y Apple Silicon (arm64)

echo "🚀 Iniciando compilación de SHW Reader para macOS..."

# Limpiar directorio de distribución anterior
echo "🧹 Limpiando builds anteriores..."
rm -rf dist/

# Verificar que las dependencias estén instaladas
echo "📦 Verificando dependencias de Python..."
pip3 install -r requirements.txt

echo "📦 Verificando dependencias de Node.js..."
npm install

# Compilar para Intel (x64)
echo "🔧 Compilando para macOS Intel (x64)..."
npm run dist:mac-intel

# Verificar si la compilación Intel fue exitosa
if [ $? -eq 0 ]; then
    echo "✅ Compilación Intel completada exitosamente"
else
    echo "❌ Error en la compilación Intel"
    exit 1
fi

# Compilar para Apple Silicon (arm64)
echo "🔧 Compilando para macOS Apple Silicon (arm64)..."
npm run dist:mac-silicon

# Verificar si la compilación Apple Silicon fue exitosa
if [ $? -eq 0 ]; then
    echo "✅ Compilación Apple Silicon completada exitosamente"
else
    echo "❌ Error en la compilación Apple Silicon"
    exit 1
fi

# Mostrar archivos generados
echo "📁 Archivos generados en el directorio dist/:"
ls -la dist/

echo "🎉 ¡Compilación completada! Los archivos están en el directorio 'dist/':"
echo "   📱 Intel (x64): SHW Reader-*-mac-x64.dmg"
echo "   📱 Apple Silicon (arm64): SHW Reader-*-mac-arm64.dmg"
echo ""
echo "💡 También puedes ejecutar:"
echo "   - npm run dist:mac-universal  (para crear un build universal)"
echo "   - npm run dist:mac            (para crear ambas arquitecturas)"
