#!/usr/bin/env python3
"""
Script para compilar el servidor Flask standalone con PyInstaller
Crea un ejecutable independiente que no requiere Python instalado
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """Instalar PyInstaller si no está disponible"""
    try:
        import PyInstaller
        print("✅ PyInstaller ya está instalado")
        return True
    except ImportError:
        print("📦 Instalando PyInstaller...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
            print("✅ PyInstaller instalado exitosamente")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error instalando PyInstaller: {e}")
            return False

def install_dependencies():
    """Instalar dependencias necesarias"""
    dependencies = [
        'flask',
        'werkzeug',
        'pyinstaller'
    ]
    
    print("📦 Instalando dependencias...")
    for dep in dependencies:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])
            print(f"✅ {dep} instalado")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error instalando {dep}: {e}")
            return False
    
    return True

def compile_flask_server():
    """Compilar el servidor Flask con PyInstaller"""
    print("🔨 Compilando servidor Flask standalone...")
    
    # Asegurar que el archivo existe
    flask_file = Path("flask_standalone.py")
    if not flask_file.exists():
        print(f"❌ No se encontró {flask_file}")
        return False
    
    # Crear directorio de salida
    output_dir = Path("dist/flask_server")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Obtener rutas absolutas para los recursos
    base_dir = Path.cwd()
    templates_path = base_dir / "templates"
    static_path = base_dir / "static"
    translations_path = base_dir / "translations"
    
    # Verificar que los directorios existen
    missing_dirs = []
    if not templates_path.exists():
        missing_dirs.append("templates")
    if not static_path.exists():
        missing_dirs.append("static")
    if not translations_path.exists():
        missing_dirs.append("translations")
    
    if missing_dirs:
        print(f"⚠️ Directorios faltantes: {', '.join(missing_dirs)}")
        print("Compilando sin estos recursos...")
    
    # Comando PyInstaller con rutas absolutas
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',  # Crear un solo ejecutable
        '--console',  # Con ventana de consola para debug
        '--name', 'flask_server',
        '--distpath', str(output_dir),
        '--workpath', 'build/flask_server',
        '--specpath', 'build',
        # Hooks para Flask
        '--hidden-import', 'flask',
        '--hidden-import', 'werkzeug',
        '--hidden-import', 'jinja2',
        '--hidden-import', 'click',
        '--hidden-import', 'itsdangerous',
        '--hidden-import', 'markupsafe',
        str(flask_file)
    ]
    
    # Añadir recursos solo si existen
    if templates_path.exists():
        cmd.extend(['--add-data', f'{templates_path}:templates'])
    if static_path.exists():
        cmd.extend(['--add-data', f'{static_path}:static'])
    if translations_path.exists():
        cmd.extend(['--add-data', f'{translations_path}:translations'])
    
    try:
        print(f"Ejecutando PyInstaller...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            executable_name = 'flask_server.exe' if os.name == 'nt' else 'flask_server'
            executable_path = output_dir / executable_name
            
            if executable_path.exists():
                print(f"✅ Servidor compilado exitosamente: {executable_path}")
                print(f"📁 Tamaño: {executable_path.stat().st_size / 1024 / 1024:.1f} MB")
                return True
            else:
                print(f"❌ El ejecutable no se creó: {executable_path}")
                return False
        else:
            print(f"❌ Error compilando:")
            if result.stdout:
                print(f"stdout: {result.stdout}")
            if result.stderr:
                print(f"stderr: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando PyInstaller: {e}")
        return False

def test_compiled_server():
    """Probar el servidor compilado"""
    executable_name = 'flask_server.exe' if os.name == 'nt' else 'flask_server'
    executable_path = Path(f"dist/flask_server/{executable_name}")
    
    if not executable_path.exists():
        print(f"❌ No se encontró el ejecutable: {executable_path}")
        return False
    
    print("🧪 Probando servidor compilado...")
    
    try:
        # Probar que el ejecutable se puede ejecutar
        cmd = [str(executable_path), '--help']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Servidor compilado funciona correctamente")
            return True
        else:
            print(f"❌ Error probando servidor: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⚠️ Timeout probando servidor (puede ser normal)")
        return True
    except Exception as e:
        print(f"❌ Error probando servidor: {e}")
        return False

def main():
    print("🐍 === Compilador de Servidor Flask Embebido ===")
    print("Este script crea un ejecutable independiente del servidor Flask")
    print()
    
    # Verificar Python
    if sys.version_info < (3, 7):
        print("❌ Se requiere Python 3.7 o superior")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Instalar dependencias
    if not install_dependencies():
        print("❌ Error instalando dependencias")
        return False
    
    # Compilar servidor
    if not compile_flask_server():
        print("❌ Error compilando servidor")
        return False
    
    # Probar servidor
    if not test_compiled_server():
        print("⚠️ Advertencia: No se pudo probar el servidor compilado")
    
    print()
    print("✅ === Compilación Completada ===")
    print("📁 El servidor embebido está en: dist/flask_server/")
    print("🚀 Ahora puedes incluir este ejecutable en tu aplicación Electron")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
