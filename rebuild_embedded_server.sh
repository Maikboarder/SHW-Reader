#!/bin/bash

# Script para recompilar el servidor Flask embebido
# Este script debe ejecutarse cuando se modifique flask_standalone.py

echo "🚀 === Recompilador de Servidor Embebido ==="
echo "Compilando servidor Flask standalone..."
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "flask_standalone.py" ]; then
    echo "❌ Error: No se encuentra flask_standalone.py"
    echo "Ejecute este script desde el directorio raíz del proyecto"
    exit 1
fi

# Verificar que Python está disponible
if [ ! -d ".venv" ]; then
    echo "❌ Error: No se encuentra el entorno virtual .venv"
    echo "Ejecute primero: python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activar entorno virtual y compilar
echo "🔧 Activando entorno virtual..."
source .venv/bin/activate

echo "📦 Compilando servidor embebido..."
python build_flask_embedded.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ === Compilación Completada ==="
    echo "📁 Ejecutable disponible en: dist/flask_server/flask_server"
    echo "🚀 Puede probar la aplicación con: npm start"
    echo ""
    echo "📋 Para distribuir:"
    echo "   - Incluya dist/flask_server/ completo en el empaquetado"
    echo "   - El ejecutable debe estar en la misma ubicación relativa"
else
    echo ""
    echo "❌ Error en la compilación"
    echo "Revise los mensajes de error anteriores"
    exit 1
fi
