#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de construcción para crear ejecutable independiente de Flask
para la aplicación SHW Reader en Windows
"""

import PyInstaller.__main__
import sys
import os

def build_flask_executable():
    """Construye el ejecutable de Flask usando PyInstaller"""
    
    # Configuración de PyInstaller
    pyinstaller_args = [
        'app_desktop.py',
        '--onefile',
        '--console',
        '--name=shw-reader-backend',
        '--distpath=dist/flask',
        '--workpath=build/flask',
        '--specpath=build',
        '--add-data=templates:templates',
        '--add-data=static:static', 
        '--add-data=translations:translations',
        '--hidden-import=flask',
        '--hidden-import=werkzeug',
        '--hidden-import=openpyxl',
        '--hidden-import=python-docx',
        '--hidden-import=reportlab',
        '--hidden-import=json',
        '--hidden-import=os',
        '--collect-all=flask',
        '--collect-all=werkzeug',
        '--noconfirm'
    ]
    
    print("Construyendo ejecutable Flask independiente...")
    PyInstaller.__main__.run(pyinstaller_args)
    print("¡Ejecutable Flask creado exitosamente!")

if __name__ == '__main__':
    build_flask_executable()
