#!/bin/bash
# Script para empaquetar el backend Flask como ejecutable standalone para Mac ARM64 (Apple Silicon)
# Requiere pyinstaller instalado en el entorno de Python

set -e

APP=app_desktop.py
NAME=shwreader-backend
DIST_DIR=dist_mac_arm64

# Limpieza previa
echo "Limpiando directorios previos..."
rm -rf build/ $DIST_DIR/ __pycache__/

# Empaquetar con pyinstaller
echo "Empaquetando con PyInstaller..."
pyinstaller --onefile --name $NAME --distpath $DIST_DIR --add-data "templates:templates" --add-data "static:static" --add-data "translations:translations" $APP

echo "Ejecutable generado en $DIST_DIR/$NAME"
