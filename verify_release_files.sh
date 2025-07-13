#!/bin/bash

# Script de verificación antes de crear el release
echo "🔍 Verificando archivos para el release de SHW Reader v1.0.0..."
echo ""

# Directorio de distribución
DIST_DIR="/Users/imaik/Documents/SHW-Reader/dist"

# Archivos esperados
FILES=(
    "SHW Reader Setup 1.0.0.exe"
    "SHW Reader 1.0.0.exe"
    "SHW Reader-1.0.0.dmg"
    "SHW Reader-1.0.0-arm64.dmg"
    "SHW Reader-1.0.0-mac.zip"
    "SHW Reader-1.0.0-arm64-mac.zip"
)

echo "📁 Verificando archivos en: $DIST_DIR"
echo ""

# Verificar que cada archivo existe
all_files_found=true
for file in "${FILES[@]}"; do
    if [ -f "$DIST_DIR/$file" ]; then
        size=$(du -h "$DIST_DIR/$file" | cut -f1)
        echo "✅ $file ($size)"
    else
        echo "❌ $file (NO ENCONTRADO)"
        all_files_found=false
    fi
done

echo ""

if [ "$all_files_found" = true ]; then
    echo "🎉 ¡Todos los archivos están listos para el release!"
    echo ""
    echo "📋 Próximos pasos:"
    echo "1. Ve a GitHub.com y navega a tu repositorio"
    echo "2. Haz clic en 'Releases'"
    echo "3. Haz clic en 'Create a new release'"
    echo "4. Usa el tag 'v1.0.0'"
    echo "5. Copia la descripción de 'create_github_release.md'"
    echo "6. Sube los archivos listados arriba"
    echo "7. Publica el release"
    echo ""
    echo "📖 Para instrucciones detalladas, consulta: create_github_release.md"
else
    echo "⚠️  Faltan algunos archivos. Ejecuta 'npm run build' para regenerarlos."
fi

echo ""
echo "🔗 Tamaño total de archivos para subir:"
total_size=$(du -h "$DIST_DIR"/*.exe "$DIST_DIR"/*.dmg "$DIST_DIR"/*.zip 2>/dev/null | awk '{sum += $1} END {print sum "M"}' 2>/dev/null || echo "calculando...")
echo "   Aproximadamente: $total_size"
