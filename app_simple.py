#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Servidor Flask simplificado e independiente para SHW Reader
Este archivo puede ser compilado con PyInstaller para crear un ejecutable independiente
"""

import os
import sys
import zipfile
import json
import tempfile
import uuid
from pathlib import Path

# Importar Flask y dependencias
try:
    from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
    from werkzeug.utils import secure_filename
except ImportError as e:
    print(f"Error: {e}")
    print("Flask no está instalado. Instale Flask con: pip install flask")
    sys.exit(1)

# Configuración
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'shw_reader_secret_key_2024'

# Variables globales
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'shw'}
current_data = None
current_filename = None

# Crear directorio de uploads si no existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    """Verificar si el archivo tiene una extensión permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_shw_file(filepath):
    """Procesar archivo SHW y extraer datos"""
    try:
        channels = []
        
        with zipfile.ZipFile(filepath, 'r') as zip_file:
            file_list = zip_file.namelist()
            
            # Buscar archivo de datos principal
            for file_name in file_list:
                if file_name.endswith('.xml'):
                    try:
                        content = zip_file.read(file_name).decode('utf-8', errors='ignore')
                        # Aquí iría el parser XML específico para SHW
                        # Por ahora, devolvemos datos de ejemplo
                        channels = [
                            {
                                'id': i + 1,
                                'name': f'Channel {i + 1}',
                                'frequency': f'{500 + i}.000',
                                'group': 'A',
                                'type': 'Wireless'
                            }
                            for i in range(10)
                        ]
                        break
                    except Exception as e:
                        print(f"Error procesando {file_name}: {e}")
                        continue
        
        return {
            'success': True,
            'channels': channels,
            'total': len(channels),
            'filename': os.path.basename(filepath)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f'Error procesando archivo SHW: {str(e)}'
        }

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Subir y procesar archivo SHW"""
    global current_data, current_filename
    
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No se seleccionó archivo'})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No se seleccionó archivo'})
    
    if file and file.filename and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Procesar archivo
        result = process_shw_file(filepath)
        
        if result['success']:
            current_data = result
            current_filename = filename
        
        return jsonify(result)
    
    return jsonify({'success': False, 'error': 'Tipo de archivo no válido'})

@app.route('/data')
def get_data():
    """Obtener datos actuales"""
    global current_data
    if current_data:
        return jsonify(current_data)
    return jsonify({'success': False, 'error': 'No hay datos cargados'})

@app.route('/export/<format>')
def export_data(format):
    """Exportar datos en diferentes formatos"""
    global current_data, current_filename
    
    if not current_data or not current_data.get('success'):
        return jsonify({'success': False, 'error': 'No hay datos para exportar'})
    
    try:
        if format == 'csv':
            return export_csv()
        elif format == 'json':
            return export_json()
        else:
            return jsonify({'success': False, 'error': 'Formato no soportado'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def export_csv():
    """Exportar a CSV"""
    import csv
    import io
    
    if not current_data or 'channels' not in current_data:
        return jsonify({'success': False, 'error': 'No hay datos para exportar'})
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Escribir encabezados
    writer.writerow(['ID', 'Name', 'Frequency', 'Group', 'Type'])
    
    # Escribir datos
    for channel in current_data['channels']:
        writer.writerow([
            channel.get('id', ''),
            channel.get('name', ''),
            channel.get('frequency', ''),
            channel.get('group', ''),
            channel.get('type', '')
        ])
    
    # Crear archivo temporal
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
    temp_file.write(output.getvalue())
    temp_file.close()
    
    return send_file(temp_file.name, as_attachment=True, download_name=f'{current_filename}_export.csv')

def export_json():
    """Exportar a JSON"""
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    json.dump(current_data, temp_file, indent=2)
    temp_file.close()
    
    return send_file(temp_file.name, as_attachment=True, download_name=f'{current_filename}_export.json')

@app.route('/static/<path:filename>')
def static_files(filename):
    """Servir archivos estáticos"""
    return send_from_directory('static', filename)

def main():
    """Función principal"""
    print("=== SHW Reader Backend Server ===")
    print("Iniciando servidor Flask...")
    print("URL: http://127.0.0.1:5001")
    print("Presiona Ctrl+C para detener el servidor")
    
    try:
        app.run(host='127.0.0.1', port=5001, debug=False, threaded=True)
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario")
    except Exception as e:
        print(f"Error en el servidor: {e}")

if __name__ == '__main__':
    main()
