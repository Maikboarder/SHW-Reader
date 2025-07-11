#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Servidor Flask standalone para SHW Reader
Este archivo será compilado con PyInstaller para crear un ejecutable independiente
"""

import os
import sys
import zipfile
import json
import tempfile
import uuid
from pathlib import Path
import argparse

# Importar Flask y dependencias
try:
    from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
    from werkzeug.utils import secure_filename
except ImportError as e:
    print(f"Error: {e}")
    print("Flask no está instalado. Este script debe ser compilado con PyInstaller.")
    sys.exit(1)

# Configuración
app = Flask(__name__)
app.secret_key = 'shw_reader_secret_key_2024'

# Variables globales
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'shw'}
current_data = None
current_filename = None

def init_app(port=5001, templates_dir=None, static_dir=None):
    """Inicializar la aplicación Flask con directorios personalizados"""
    global app
    
    # Detectar si estamos ejecutándose desde un ejecutable PyInstaller
    if getattr(sys, 'frozen', False):
        # Ejecutándose desde ejecutable compilado
        bundle_dir = sys._MEIPASS
        
        # Configurar directorios por defecto desde el bundle
        if not templates_dir:
            templates_dir = os.path.join(bundle_dir, 'templates')
        if not static_dir:
            static_dir = os.path.join(bundle_dir, 'static')
    else:
        # Ejecutándose desde código fuente
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Configurar directorios si existen
    if templates_dir and os.path.exists(templates_dir):
        app.template_folder = templates_dir
        print(f"✅ Templates configurados: {templates_dir}")
    else:
        print(f"⚠️ Directorio de templates no encontrado: {templates_dir}")
        
    if static_dir and os.path.exists(static_dir):
        app.static_folder = static_dir
        print(f"✅ Static configurado: {static_dir}")
    else:
        print(f"⚠️ Directorio static no encontrado: {static_dir}")
    
    # Crear directorio de uploads si no existe
    upload_path = os.path.join(os.getcwd(), UPLOAD_FOLDER)
    os.makedirs(upload_path, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = upload_path
    
    print(f"=== SHW Reader Backend Server (Standalone) ===")
    print(f"Iniciando servidor Flask embebido...")
    print(f"Puerto: {port}")
    print(f"Templates: {app.template_folder}")
    print(f"Static: {app.static_folder}")
    print(f"Uploads: {upload_path}")
    print(f"URL: http://127.0.0.1:{port}")
    print(f"Presiona Ctrl+C para detener el servidor")

def allowed_file(filename):
    """Verificar si el archivo tiene una extensión permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_shw_file(filepath):
    """Procesar archivo SHW y extraer datos"""
    try:
        channels = []
        
        with zipfile.ZipFile(filepath, 'r') as zip_file:
            file_list = zip_file.namelist()
            print(f"Archivos en SHW: {file_list}")
            
            # Buscar archivos de coordinación
            coordination_files = [f for f in file_list if f.endswith('.wwcoordination')]
            
            if not coordination_files:
                return {
                    'success': False,
                    'error': 'No se encontraron archivos de coordinación en el archivo SHW'
                }
            
            # Procesar el primer archivo de coordinación encontrado
            coord_file = coordination_files[0]
            print(f"Procesando archivo de coordinación: {coord_file}")
            
            with zip_file.open(coord_file) as coord:
                coord_data = coord.read().decode('utf-8')
                
                # Parsear el XML básico para extraer canales
                lines = coord_data.split('\n')
                channel_id = 1
                
                for line in lines:
                    line = line.strip()
                    
                    # Buscar elementos de canal
                    if '<Channel ' in line or '<channel ' in line:
                        try:
                            # Extraer atributos básicos
                            name = 'Canal ' + str(channel_id)
                            frequency = '500.000'  # Valor por defecto
                            group = 'A'
                            device_type = 'Wireless'
                            band = 'UHF'
                            
                            # Buscar nombre en el XML
                            if 'Name="' in line:
                                start = line.find('Name="') + 6
                                end = line.find('"', start)
                                if end > start:
                                    name = line[start:end]
                            
                            # Buscar frecuencia
                            if 'Frequency="' in line:
                                start = line.find('Frequency="') + 11
                                end = line.find('"', start)
                                if end > start:
                                    freq_val = line[start:end]
                                    try:
                                        # Convertir a MHz
                                        freq_hz = float(freq_val)
                                        frequency = f"{freq_hz / 1000000:.3f}"
                                    except:
                                        frequency = freq_val
                            
                            # Buscar grupo
                            if 'Group="' in line:
                                start = line.find('Group="') + 7
                                end = line.find('"', start)
                                if end > start:
                                    group = line[start:end]
                            
                            channel = {
                                'id': channel_id,
                                'name': name,
                                'frequency': frequency,
                                'group': group,
                                'device_type': device_type,
                                'band': band
                            }
                            
                            channels.append(channel)
                            channel_id += 1
                            
                        except Exception as e:
                            print(f"Error procesando línea: {line[:100]}... Error: {e}")
                            continue
        
        return {
            'success': True,
            'channels': channels,
            'total': len(channels),
            'filename': os.path.basename(filepath)
        }
        
    except Exception as e:
        print(f"Error procesando archivo SHW: {e}")
        return {
            'success': False,
            'error': f'Error procesando archivo SHW: {str(e)}'
        }

@app.route('/')
def index():
    """Página principal"""
    try:
        return render_template('index.html')
    except Exception as e:
        # Fallback HTML básico si no hay templates
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>SHW Reader</title>
            <meta charset="utf-8">
        </head>
        <body>
            <h1>SHW Reader - Servidor Embebido</h1>
            <p>El servidor Python embebido está funcionando correctamente.</p>
            <p>Error cargando template: {e}</p>
        </body>
        </html>
        '''

@app.route('/static/<path:filename>')
def static_files(filename):
    """Servir archivos estáticos"""
    try:
        static_folder = app.static_folder or 'static'
        return send_from_directory(static_folder, filename)
    except Exception as e:
        return f"Error: {e}", 404

@app.route('/upload', methods=['POST'])
def upload_file():
    """Manejar subida de archivos SHW"""
    global current_data, current_filename
    
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No se seleccionó archivo'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No se seleccionó archivo'})
        
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = str(int(time.time())) if 'time' in globals() else str(uuid.uuid4())[:8]
            unique_filename = f"{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            
            file.save(filepath)
            print(f"Archivo guardado: {filepath}")
            
            # Procesar el archivo SHW
            result = process_shw_file(filepath)
            
            if result['success']:
                current_data = result['channels']
                current_filename = filename
                print(f"Archivo procesado exitosamente: {len(result['channels'])} canales encontrados")
            
            # Limpiar archivo temporal
            try:
                os.remove(filepath)
            except:
                pass
            
            return jsonify(result)
        
        return jsonify({'success': False, 'error': 'Tipo de archivo no permitido'})
        
    except Exception as e:
        print(f"Error en upload: {e}")
        return jsonify({'success': False, 'error': f'Error procesando archivo: {str(e)}'})

@app.route('/data')
def get_data():
    """Obtener datos actuales"""
    global current_data
    if current_data:
        return jsonify({
            'success': True,
            'channels': current_data,
            'total': len(current_data),
            'filename': current_filename
        })
    return jsonify({'success': False, 'error': 'No hay datos cargados'})

@app.route('/export/<format>')
def export_data(format):
    """Exportar datos (funcionalidad básica)"""
    global current_data
    
    if not current_data:
        return jsonify({'success': False, 'error': 'No hay datos para exportar'})
    
    # Por ahora, solo CSV básico
    if format == 'csv':
        try:
            import io
            import csv
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Encabezados
            writer.writerow(['ID', 'Name', 'Frequency', 'Group', 'Device Type', 'Band'])
            
            # Datos
            for channel in current_data:
                writer.writerow([
                    channel.get('id', ''),
                    channel.get('name', ''),
                    channel.get('frequency', ''),
                    channel.get('group', ''),
                    channel.get('device_type', ''),
                    channel.get('band', '')
                ])
            
            output.seek(0)
            return output.getvalue(), 200, {
                'Content-Type': 'text/csv',
                'Content-Disposition': 'attachment; filename=shw_export.csv'
            }
            
        except Exception as e:
            return jsonify({'success': False, 'error': f'Error exportando CSV: {str(e)}'})
    
    return jsonify({'success': False, 'error': f'Formato {format} no soportado en servidor embebido'})

@app.route('/api/translations/<lang>')
def get_translations(lang):
    """Obtener traducciones"""
    try:
        # Buscar directorio de traducciones
        if getattr(sys, 'frozen', False):
            # Ejecutándose desde ejecutable compilado
            translations_dir = os.path.join(sys._MEIPASS, 'translations')
        else:
            # Ejecutándose desde código fuente
            translations_dir = os.path.join(os.path.dirname(__file__), 'translations')
            if not os.path.exists(translations_dir):
                translations_dir = 'translations'
        
        translation_file = os.path.join(translations_dir, f'{lang}.json')
        
        if os.path.exists(translation_file):
            with open(translation_file, 'r', encoding='utf-8') as f:
                translations = json.load(f)
            return jsonify(translations)
        else:
            # Fallback a español
            es_file = os.path.join(translations_dir, 'es.json')
            if os.path.exists(es_file):
                with open(es_file, 'r', encoding='utf-8') as f:
                    translations = json.load(f)
                return jsonify(translations)
            else:
                # Fallback básico
                return jsonify({
                    'menu': {
                        'file': 'Archivo',
                        'open_file': 'Abrir archivo',
                        'about': 'Acerca de'
                    }
                })
            
    except Exception as e:
        print(f"Error cargando traducciones para {lang}: {e}")
    
    return jsonify({'error': 'Traducciones no encontradas'}), 404

if __name__ == '__main__':
    import time
    
    # Parsear argumentos de línea de comandos
    parser = argparse.ArgumentParser(description='SHW Reader Backend Server')
    parser.add_argument('--port', type=int, default=5001, help='Puerto del servidor')
    parser.add_argument('--templates', type=str, help='Directorio de templates')
    parser.add_argument('--static', type=str, help='Directorio de archivos estáticos')
    
    args = parser.parse_args()
    
    # Inicializar la aplicación
    init_app(args.port, args.templates, args.static)
    
    # Ejecutar el servidor
    try:
        app.run(host='127.0.0.1', port=args.port, debug=False, threaded=True)
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario")
    except Exception as e:
        print(f"Error ejecutando servidor: {e}")
        sys.exit(1)
