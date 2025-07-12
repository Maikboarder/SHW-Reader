from flask import Flask, render_template, request, jsonify, send_file
import xml.etree.ElementTree as ET
import os
import json
import csv
import io
import tempfile
from werkzeug.utils import secure_filename
import signal
import sys
from datetime import datetime

app = Flask(__name__, template_folder='templates', static_folder='static')

# Configuración de idiomas y caché de traducciones
language_config = {
    'languages': ['es', 'en', 'fr', 'de', 'it', 'pt', 'ca', 'gl', 'eu'],
    'defaultLanguage': 'es',
    'fallbackLanguage': 'es'
}
translations_cache = {}

def load_translations():
    translations_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'translations')
    for lang in language_config['languages']:
        path = os.path.join(translations_dir, f'{lang}.json')
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                translations_cache[lang] = json.load(f)

def get_translation(key, lang, fallback=None, **kwargs):
    d = translations_cache.get(lang) or translations_cache.get(language_config['fallbackLanguage'], {})
    value = d
    for part in key.split('.'):
        value = value.get(part, {}) if isinstance(value, dict) else {}
    if not value or isinstance(value, dict):
        value = fallback or key
    if kwargs:
        try:
            value = value.format(**kwargs)
        except Exception:
            pass
    return value

def parse_shw_file(filepath):
    devices = []
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        for device in root.findall('.//device'):
            device_info = {
                'device_name': device.findtext('device_name', 'N/A'),
                'model': device.findtext('model', 'N/A'),
                'series': device.findtext('series', 'N/A'),
                'zone': device.findtext('zone', 'N/A'),
                'band': device.findtext('band', 'N/A'),
                'channels': []
            }
            for channel in device.findall('channel'):
                channel_info = {
                    'name': channel.findtext('channel_name', 'N/A'),
                    'frequency': 'N/A'
                }
                freq_elem = channel.find('frequency')
                if freq_elem is not None and freq_elem.text:
                    try:
                        freq_mhz = int(freq_elem.text) / 1000
                        channel_info['frequency'] = f"{freq_mhz:.3f}"
                    except Exception:
                        pass
                device_info['channels'].append(channel_info)
            devices.append(device_info)
        return devices
    except Exception:
        return []
## Limpieza: eliminadas importaciones y banderas de exportación a Excel, Word y PDF

# Determinar las rutas correctas para templates y static
import os
current_dir = os.path.dirname(os.path.abspath(__file__))

# Configurar las rutas de templates y static
template_dir = os.path.join(current_dir, 'templates')
static_dir = os.path.join(current_dir, 'static')
upload_dir = os.path.join(current_dir, 'uploads')
translations_dir = os.path.join(current_dir, 'translations')

# Verificar que existan los directorios, si no, crearlos
os.makedirs(template_dir, exist_ok=True)
os.makedirs(static_dir, exist_ok=True)
os.makedirs(upload_dir, exist_ok=True)
os.makedirs(translations_dir, exist_ok=True)

print(f"Directorio actual: {current_dir}")
print(f"Directorio de templates: {template_dir}")
print(f"Directorio de static: {static_dir}")


## Limpieza: eliminados todos los endpoints y lógica de exportación a Excel, Word y PDF

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/languages')
def get_languages():
    """Get available languages"""
    return jsonify({
        'languages': language_config.get('languages', []),
        'defaultLanguage': language_config.get('defaultLanguage', 'es')
    })

@app.route('/api/translations/<lang>')
def get_translations(lang):
    """Get translations for a specific language"""
    if lang in translations_cache:
        return jsonify(translations_cache[lang])
    else:
        # Return fallback language
        fallback_lang = language_config.get('fallbackLanguage', 'es')
        return jsonify(translations_cache.get(fallback_lang, {}))

@app.route('/api/set_language', methods=['POST'])
def set_language():
    """Set user's preferred language (for future server-side features)"""
    data = request.get_json()
    lang = data.get('language', 'es')
    
    # Get the native name of the language
    language_names = {
        'es': 'Español',
        'en': 'English',
        'fr': 'Français',
        'de': 'Deutsch',
        'it': 'Italiano',
        'pt': 'Português',
        'ca': 'Català',
        'gl': 'Galego',
        'eu': 'Euskera'
    }
    language_name = language_names.get(lang, lang)
    
    # In a real app, you might save this to user preferences
    # For now, just acknowledge the change
    return jsonify({
        'success': True,
        'language': lang,
        'message': get_translation('messages.language_changed', lang, language=language_name)
    })

@app.route('/load_file_path', methods=['POST'])
def load_file_path():
    """Load a .shw file from a given file path (for Electron file dialog)"""
    data = request.get_json()
    file_path = data.get('file_path')
    
    if not file_path:
        return jsonify({'error': 'No file path provided'}), 400
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    
    if not file_path.lower().endswith('.shw'):
        return jsonify({'error': 'Invalid file type. Only .shw files are allowed.'}), 400
    
    try:
        # Parse the file directly from the path
        devices = parse_shw_file(file_path)
        
        # Convert to flat structure for table display
        rows = []
        for device in devices:
            device_display_name = f"{device.get('device_name', 'Dispositivo')} ({device.get('model', 'N/A')})"
            zone = device.get('zone', 'N/A')
            band = device.get('band', 'N/A')

            if device['channels']:
                for i, channel in enumerate(device['channels']):
                    name = channel.get('name', 'N/A')
                    freq = channel.get('frequency', 'N/A')
                    
                    # For the first channel, show device name. For others, leave it blank.
                    if i == 0:
                        rows.append({
                            'id': f"{len(rows)}",
                            'device': device_display_name,
                            'channel': name,
                            'frequency': freq,
                            'zone': zone,
                            'band': band
                        })
                    else:
                        rows.append({
                            'id': f"{len(rows)}",
                            'device': '',
                            'channel': name,
                            'frequency': freq,
                            'zone': zone,
                            'band': band
                        })
            else:
                # If a device has no channels, still show the device
                rows.append({
                    'id': f"{len(rows)}",
                    'device': device_display_name,
                    'channel': 'N/A',
                    'frequency': 'N/A',
                    'zone': zone,
                    'band': band
                })
        
        return jsonify({
            'success': True,
            'devices': len(devices),
            'rows': len(rows),
            'data': rows,
            'filename': os.path.basename(file_path)
        })
        
    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and file.filename and file.filename.lower().endswith('.shw'):
        # Usar directorio temporal para archivos
        with tempfile.NamedTemporaryFile(delete=False, suffix='.shw') as temp_file:
            file.save(temp_file.name)
            filepath = temp_file.name
        
        try:
            # Parse the file
            devices = parse_shw_file(filepath)
            
            # Convert to flat structure for table display
            rows = []
            for device in devices:
                device_display_name = f"{device.get('device_name', 'Dispositivo')} ({device.get('model', 'N/A')})"
                zone = device.get('zone', 'N/A')
                band = device.get('band', 'N/A')

                if device['channels']:
                    for i, channel in enumerate(device['channels']):
                        name = channel.get('name', 'N/A')
                        freq = channel.get('frequency', 'N/A')
                        
                        # For the first channel, show device name. For others, leave it blank.
                        if i == 0:
                            rows.append({
                                'id': f"{len(rows)}",
                                'device': device_display_name,
                                'channel': name,
                                'frequency': freq,
                                'zone': zone,
                                'band': band
                            })
                        else:
                            rows.append({
                                'id': f"{len(rows)}",
                                'device': '',
                                'channel': name,
                                'frequency': freq,
                                'zone': zone,
                                'band': band
                            })
                else:
                    # If a device has no channels, still show the device
                    rows.append({
                        'id': f"{len(rows)}",
                        'device': device_display_name,
                        'channel': 'N/A',
                        'frequency': 'N/A',
                        'zone': zone,
                        'band': band
                    })
            
            return jsonify({
                'success': True,
                'devices': len(devices),
                'rows': len(rows),
                'data': rows
            })
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(filepath)
            except:
                pass
    
    return jsonify({'error': 'Invalid file type. Only .shw files are allowed.'}), 400

@app.route('/update_row', methods=['POST'])
def update_row():
    """Update a row's data"""
    data = request.get_json()
    # In a real application, you would save this to a database
    # For now, just return success
    return jsonify({'success': True})

@app.route('/export_csv', methods=['POST'])
def export_csv():
    """Export table data to CSV"""
    data = request.get_json()
    rows = data.get('rows', [])
    lang = data.get('language', 'es')
    
    if not rows:
        error_msg = get_translation('messages.no_data', lang)
        return jsonify({'error': error_msg}), 400
    
    # Create CSV content
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header with translations
    headers = [
        get_translation('table_headers.channel', lang),
        get_translation('table_headers.frequency', lang),
        get_translation('table_headers.rf_zone', lang),
        get_translation('table_headers.device_model', lang),
        get_translation('table_headers.band', lang)
    ]
    writer.writerow(headers)
    
    # Write data
    for row in rows:
        freq_display = f"{row['frequency']} MHz" if row['frequency'] != 'N/A' else 'N/A'
        writer.writerow([
            row['channel'], 
            freq_display,
            row['zone'],
            row['device'],
            row['band']
        ])
    
    csv_content = output.getvalue()
    output.close()
    
    return jsonify({
        'success': True,
        'csv_data': csv_content,
        'filename': 'shw_data_export.csv'
    })

    
    # Create document
    doc = Document()
    
    # Add title
    title = doc.add_heading('SHW Reader - ' + get_translation('export.data_export', lang, fallback='Data Export'), 0)
    
    # Add export info
    info_para = doc.add_paragraph()
    info_para.add_run(f'{get_translation("export.generated_on", lang, fallback="Generated on")}: ')
    info_para.add_run(datetime.now().strftime('%Y-%m-%d %H:%M:%S')).bold = True
    info_para.add_run(f'\n{get_translation("export.total_records", lang, fallback="Total records")}: ');
    info_para.add_run(str(len(rows))).bold = True
    
    # Add some space
    doc.add_paragraph()
    
    # Headers with translations
    headers = [
        get_translation('table_headers.channel', lang),
        get_translation('table_headers.frequency', lang),
        get_translation('table_headers.rf_zone', lang),
        get_translation('table_headers.device_model', lang),
        get_translation('table_headers.band', lang)
    ]
    
    # Create table
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = 'Table Grid'
    
    # Add header row
    hdr_cells = table.rows[0].cells
    for i, header in enumerate(headers):
        hdr_cells[i].text = header
        # Make header bold
        for paragraph in hdr_cells[i].paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
    
    # Add data rows
    for row in rows:
        freq_display = f"{row['frequency']} MHz" if row['frequency'] != 'N/A' else 'N/A'
        data_row = [
            row['channel'],
            freq_display,
            row['zone'],
            row['device'],
            row['band']
        ]
        
        row_cells = table.add_row().cells
        for i, value in enumerate(data_row):
            row_cells[i].text = str(value)
    
    # Set column widths
    for column in table.columns:
        for cell in column.cells:
            cell.width = Inches(1.5)
    
    # Save to temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.docx')
    doc.save(temp_file.name)
    temp_file.close()
    
    try:
        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name=f'shw_data_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.docx',
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    finally:
        # Clean up temp file after a delay
        def cleanup():
            try:
                os.unlink(temp_file.name)
            except:
                pass
        
        import threading
        timer = threading.Timer(10.0, cleanup)
        timer.start()


def signal_handler(sig, frame):
    print('\\nCerrando servidor Flask...')
    sys.exit(0)

if __name__ == '__main__':
    # Configurar manejador de señales para cierre limpio
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Cargar traducciones antes de iniciar el servidor
    print("🌐 Cargando traducciones...")
    load_translations()
    print(f"✅ Traducciones cargadas para {len(translations_cache)} idiomas")
    
    port = int(os.environ.get('PORT', 5001))
    print("🚀 Iniciando SHW Reader Server...")
    print(f"🌐 Servidor disponible en: http://localhost:{port}")
    
    # Ejecutar en modo de producción para la app de escritorio
    app.run(host='127.0.0.1', port=port, debug=False, use_reloader=False)
