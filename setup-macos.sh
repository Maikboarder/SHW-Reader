#!/bin/bash

# Script de instalación para SHW Reader macOS App
echo "🚀 Configurando SHW Reader para macOS..."

# Verificar si Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "❌ Node.js no está instalado."
    echo "Por favor, instala Node.js desde: https://nodejs.org/"
    exit 1
fi

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Python no está instalado."
    echo "Por favor, instala Python desde: https://python.org/"
    exit 1
fi

# Verificar si Flask está instalado
echo "🔍 Verificando Flask..."
if ! python3 -c "import flask" 2>/dev/null && ! python -c "import flask" 2>/dev/null; then
    echo "📦 Instalando Flask..."
    pip3 install flask || pip install flask
fi

# Instalar dependencias de Node.js
echo "📦 Instalando dependencias de Electron..."
npm install

# Crear directorio de assets si no existe
mkdir -p assets

# Crear un icono temporal si no existe
if [ ! -f "assets/icon.png" ]; then
    echo "🎨 Creando icono temporal..."
    # Usar un icono predeterminado o crearlo
    # Por ahora, creamos un archivo vacío que luego se puede reemplazar
    touch assets/icon.png
fi

echo "✅ Configuración completada!"
echo ""
echo "📖 Comandos disponibles:"
echo "  npm start          - Ejecutar la app en modo desarrollo"
echo "  npm run build      - Compilar la app para distribución"
echo "  npm run pack       - Empaquetar sin crear instalador"
echo ""
echo "🚀 Para probar la app, ejecuta: npm start"
