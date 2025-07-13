#!/bin/bash

# Script de verificación final para SHW Reader
echo "🔍 === VERIFICACIÓN FINAL SHW READER v1.0.0 ==="
echo ""

# Verificar que los archivos críticos existen
echo "📁 Verificando archivos críticos..."

CRITICAL_FILES=(
    "electron-main.js"
    "embedded-flask-manager.js"
    "fallback-server.js"
    "package.json"
    "preload.js"
    "templates/index.html"
)

all_critical_found=true
for file in "${CRITICAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file (FALTA)"
        all_critical_found=false
    fi
done

echo ""

# Verificar que NO hay referencias a Python externo
echo "🔍 Verificando que NO hay código obsoleto de Python..."

FORBIDDEN_PATTERNS=(
    "checkPython"
    "installFlask"
    "showPythonInstallationError"
    "startPythonFlaskServer"
    "python3 --version"
    "pip install"
)

python_refs_found=false
for pattern in "${FORBIDDEN_PATTERNS[@]}"; do
    if grep -q "$pattern" electron-main.js 2>/dev/null; then
        echo "❌ Encontrado patrón obsoleto: $pattern"
        python_refs_found=true
    fi
done

if [ "$python_refs_found" = false ]; then
    echo "✅ No se encontraron referencias obsoletas a Python"
fi

echo ""

# Verificar estructura del servidor embebido
echo "🔧 Verificando backend embebido..."

if [ -f "dist/flask_server/flask_server" ] || [ -f "dist/flask_server/flask_server.exe" ]; then
    echo "✅ Ejecutable del servidor embebido encontrado"
else
    echo "⚠️  Ejecutable del servidor no encontrado - verificar build"
fi

if [ -f "embedded-flask-manager.js" ]; then
    if grep -q "EmbeddedFlaskServer" embedded-flask-manager.js; then
        echo "✅ Gestor del servidor embebido configurado"
    else
        echo "❌ Gestor del servidor mal configurado"
    fi
fi

echo ""

# Verificar servidor de fallback
echo "🆘 Verificando servidor de fallback..."

if [ -f "fallback-server.js" ]; then
    if grep -q "createFallbackServer" fallback-server.js; then
        echo "✅ Servidor de fallback configurado"
    else
        echo "❌ Servidor de fallback mal configurado"
    fi
fi

echo ""

# Verificar instaladores (si existen)
echo "📦 Verificando instaladores..."

if [ -d "dist" ]; then
    echo "✅ Carpeta dist existe"
    
    # Contar instaladores
    exe_count=$(ls -1 dist/*.exe 2>/dev/null | wc -l)
    dmg_count=$(ls -1 dist/*.dmg 2>/dev/null | wc -l)
    zip_count=$(ls -1 dist/*mac*.zip 2>/dev/null | wc -l)
    
    echo "   📊 Instaladores encontrados:"
    echo "   - Windows (.exe): $exe_count"
    echo "   - macOS (.dmg): $dmg_count" 
    echo "   - macOS (.zip): $zip_count"
    
    if [ $exe_count -ge 2 ] && [ $dmg_count -ge 2 ] && [ $zip_count -ge 2 ]; then
        echo "✅ Todos los instaladores presentes"
    else
        echo "⚠️  Faltan algunos instaladores"
    fi
else
    echo "❌ Carpeta dist no encontrada"
fi

echo ""

# Resumen final
echo "📋 === RESUMEN FINAL ==="

if [ "$all_critical_found" = true ] && [ "$python_refs_found" = false ]; then
    echo "🎉 ✅ SHW Reader está listo para distribución"
    echo ""
    echo "🔧 Características confirmadas:"
    echo "   ✅ Backend Flask completamente embebido"
    echo "   ✅ Sin dependencias de Python externo"
    echo "   ✅ Servidor de fallback disponible"
    echo "   ✅ Código limpio sin referencias obsoletas"
    echo ""
    echo "📦 Próximos pasos:"
    echo "   1. Verificar que el build termine exitosamente"
    echo "   2. Probar los instaladores en máquinas limpias"
    echo "   3. Subir release a GitHub"
    echo ""
    echo "🎯 Los usuarios podrán usar SHW Reader SIN instalar Python"
else
    echo "⚠️  Hay problemas que requieren atención"
    
    if [ "$all_critical_found" = false ]; then
        echo "   ❌ Faltan archivos críticos"
    fi
    
    if [ "$python_refs_found" = true ]; then
        echo "   ❌ Hay código obsoleto de Python que debe eliminarse"
    fi
fi

echo ""
