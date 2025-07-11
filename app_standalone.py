#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script standalone que incluye Flask embebido para Windows
Este script se ejecutará como ejecutable independiente
"""

import sys
import os
import subprocess
import tempfile
import zipfile
from pathlib import Path

# Configuración del servidor Flask embebido
FLASK_CODE = '''
import sys
import os
from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify, flash, send_from_directory
import json
import csv
import tempfile
from io import StringIO
from werkzeug.utils import secure_filename
import zipfile

app = Flask(__name__)
app.secret_key = 'shw_reader_secret_key_2024'

# Configuración
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'shw'}

# Crear carpeta de uploads si no existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file selected'})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Procesar archivo SHW
        try:
            data = process_shw_file(filepath)
            return jsonify({'success': True, 'data': data, 'filename': filename})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    return jsonify({'success': False, 'error': 'Invalid file type'})

def process_shw_file(filepath):
    """Procesa archivo SHW y extrae datos"""
    try:
        with zipfile.ZipFile(filepath, 'r') as zip_file:
            # Buscar archivos relevantes en el ZIP
            file_list = zip_file.namelist()
            
            # Extraer datos (simplificado para este ejemplo)
            data = []
            for file_name in file_list:
                if file_name.endswith('.xml') or file_name.endswith('.json'):
                    content = zip_file.read(file_name).decode('utf-8', errors='ignore')
                    # Aquí irían los parsers específicos
                    
            return {'channels': [], 'frequencies': [], 'processed': True}
    except Exception as e:
        raise Exception(f"Error processing SHW file: {str(e)}")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=False)
'''

def create_standalone_flask():
    """Crear servidor Flask standalone"""
    # Crear archivo temporal con el código Flask
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(FLASK_CODE)
        return f.name

def main():
    """Función principal"""
    try:
        # Crear servidor Flask standalone
        flask_file = create_standalone_flask()
        
        # Ejecutar servidor Flask
        print("Iniciando servidor SHW Reader...")
        subprocess.run([sys.executable, flask_file])
        
    except Exception as e:
        print(f"Error: {e}")
        input("Presiona Enter para salir...")

if __name__ == '__main__':
    main()
