#!/usr/bin/env python3
import json
import os
import glob
import re

def clean_translations():
    """Limpia todas las traducciones eliminando referencias a Excel y Word"""
    
    translation_files = glob.glob("/Users/imaik/Documents/SHW-Readerv2/SHW-Reader/translations/*.json")
    
    replacements = {
        # Español
        'a Excel': '',
        'de Excel': 'de Datos',
        'Excel': 'Datos',
        
        # Inglés
        'to Excel': '',
        'Excel': 'Data',
        
        # Francés
        'vers Excel': '',
        'Excel': 'Données',
        
        # Alemán
        'nach Excel': '',
        'Excel': 'Daten',
        
        # Italiano
        'in Excel': '',
        'Excel': 'Dati',
        
        # Portugués
        'para Excel': '',
        'Excel': 'Dados',
        
        # Euskera
        'Excel-era': '',
        'Excel': 'Datuak',
        
        # Catalán
        'a Excel': '',
        'Excel': 'Dades',
        
        # Gallego
        'a Excel': '',
        'Excel': 'Datos',
        
        # Word referencias
        'Word': '',
        'word': ''
    }
    
    for file_path in translation_files:
        if 'config.json' in file_path:
            continue
            
        print(f"Limpiando {os.path.basename(file_path)}...")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            def clean_text(text):
                if not isinstance(text, str):
                    return text
                
                # Limpiar referencias específicas a Excel
                text = re.sub(r'\s*(a|to|vers|nach|in|para|Excel-era)\s*Excel', '', text, flags=re.IGNORECASE)
                text = re.sub(r'Excel\s*(export|exportar|exporter)', 'Data export', text, flags=re.IGNORECASE)
                text = re.sub(r'Export\s*Excel', 'Export Data', text, flags=re.IGNORECASE)
                text = re.sub(r'Exportar\s*Excel', 'Exportar Datos', text, flags=re.IGNORECASE)
                text = re.sub(r'Esportatu\s*Excel', 'Esportatu Datuak', text, flags=re.IGNORECASE)
                
                # Limpiar referencias a Word
                text = re.sub(r'\s*Word\s*', ' ', text)
                text = re.sub(r'Export\s*Word', 'Export Data', text, flags=re.IGNORECASE)
                text = re.sub(r'Exportar\s*Word', 'Exportar Datos', text, flags=re.IGNORECASE)
                
                # Limpiar espacios múltiples
                text = re.sub(r'\s+', ' ', text).strip()
                
                return text
            
            def clean_dict(d):
                if isinstance(d, dict):
                    # Eliminar claves específicas
                    keys_to_remove = []
                    for key in d.keys():
                        if 'excel' in key.lower() or 'word' in key.lower():
                            keys_to_remove.append(key)
                    
                    for key in keys_to_remove:
                        del d[key]
                    
                    # Limpiar valores
                    for key, value in d.items():
                        if isinstance(value, str):
                            d[key] = clean_text(value)
                        elif isinstance(value, dict):
                            clean_dict(value)
                        elif isinstance(value, list):
                            for i, item in enumerate(value):
                                if isinstance(item, str):
                                    value[i] = clean_text(item)
                                elif isinstance(item, dict):
                                    clean_dict(item)
                
                return d
            
            # Limpiar el diccionario completo
            data = clean_dict(data)
            
            # Guardar el archivo limpio
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
            print(f"✅ {os.path.basename(file_path)} limpiado")
            
        except Exception as e:
            print(f"❌ Error limpiando {file_path}: {e}")

if __name__ == "__main__":
    clean_translations()
    print("🧹 Limpieza de traducciones completada")
