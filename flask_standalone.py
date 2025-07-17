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
    import xml.etree.ElementTree as ET
    try:
        channels = []
        exclude_models = {"ADX2", "ADX1", "ADX1M", "ADXR"}
        with open(filepath, 'r', encoding='utf-8') as f:
            xml_data = f.read()
        # Extraer solo el bloque <inventory>...</inventory>
        import re
        match = re.search(r'<inventory[\s\S]*?</inventory>', xml_data)
        if not match:
            raise Exception('No se encontró bloque <inventory> en el archivo')
        inventory_xml = match.group(0)
        # Normalizar tag de apertura
        inventory_xml = inventory_xml.replace('<inventory version="2.1">', '<inventory>')
        # Parsear XML
        root = ET.fromstring(inventory_xml)
        channel_id = 1
        for device in root.findall('device'):
            def get_text(tag, node=device):
                el = node.find(tag)
                if el is not None and el.text:
                    return el.text.strip()
                return ''
            def get_cdata(tag, node=device):
                el = node.find(tag)
                if el is not None and el.text:
                    return el.text.strip()
                return ''
            model = get_text('model')
            manufacturer = get_text('manufacturer')
            band = get_text('band')
            zone = get_text('zone')
            device_name = get_cdata('device_name')
            device_channel_name = get_cdata('channel_name')
            device_frequency_raw = get_text('frequency')
            def format_freq(freq):
                try:
                    # Si es entero, formatear como xxx,xxx
                    freq_int = int(freq)
                    return f"{freq_int//1000},{freq_int%1000:03d}"
                except:
                    return freq
            device_frequency = format_freq(device_frequency_raw) if device_frequency_raw else ''
            exclude_prefixes = ("ADX2", "ADX1", "ADX1M", "ADXR", "SBRC")
            if any(model.startswith(prefix) for prefix in exclude_prefixes):
                continue
            # Si no hay canales hijos, usar los del device
            child_channels = device.findall('channel')
            if not child_channels and (device_channel_name or device_frequency):
                name_val = device_channel_name or model or f"Canal {channel_id}"
                channel = {
                    'id': channel_id,
                    'channel_name': device_channel_name,
                    'name': name_val,
                    'frequency': device_frequency,
                    'zone': zone,
                    'model': model,
                    'manufacturer': manufacturer,
                    'band': band,
                    'device_name': device_name
                }
                channels.append(channel)
                channel_id += 1
            # Si hay canales hijos, extraer channel_name y frequency de cada uno si existen
            for idx, channel_tag in enumerate(child_channels, 1):
                color = ''
                tags = ''
                color_el = channel_tag.find('color')
                if color_el is not None and color_el.text:
                    color = color_el.text.strip()
                tags_el = channel_tag.find('tags')
                if tags_el is not None and tags_el.text:
                    tags = tags_el.text.strip()
                # Buscar <channel_name> y <frequency> aunque tengan atributos
                channel_name = device_channel_name
                for cname in channel_tag.findall('channel_name'):
                    if cname.text and cname.text.strip():
                        channel_name = cname.text.strip()
                        break
                frequency_raw = device_frequency_raw
                for freq in channel_tag.findall('frequency'):
                    if freq.text and freq.text.strip():
                        frequency_raw = freq.text.strip()
                        break
                frequency = format_freq(frequency_raw) if frequency_raw else device_frequency
                # Si no hay nombre, usar modelo y número de canal
                name_val = channel_name or model or f"Canal {channel_id}"
                # Excluir canales hijos cuyo modelo empiece por los prefijos
                exclude_prefixes = ("ADX2", "ADX1", "ADX1M", "ADXR", "SBRC")
                if any(model.startswith(prefix) for prefix in exclude_prefixes):
                    continue
                channel = {
                    'id': channel_id,
                    'channel_name': channel_name,
                    'channel': channel_name,
                    'name': name_val,
                    'frequency': frequency,
                    'zone': zone,
                    'model': model,
                    'model_type': model,
                    'manufacturer': manufacturer,
                    'band': band,
                    'device_name': device_name,
                    'color': color,
                    'tags': tags
                }
                channels.append(channel)
                channel_id += 1
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

            # Preparar respuesta para el frontend
            if result['success']:
                current_data = result['channels']
                current_filename = filename
                print(f"Archivo procesado exitosamente: {len(result['channels'])} canales encontrados")
                response = {
                    'success': True,
                    'data': result['channels'],
                    'devices': result['total'],
                    'rows': result['total'],
                    'filename': result.get('filename', filename)
                }
            else:
                response = {
                    'success': False,
                    'error': result.get('error', 'Error desconocido')
                }

            # Limpiar archivo temporal
            try:
                os.remove(filepath)
            except:
                pass

            return jsonify(response)
        
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
