#!/usr/bin/env python3
import json
import os
import glob

def clean_menu_translations():
    """Elimina las opciones de exportar Excel y Word del menú en todos los archivos de traducción."""
    translation_files = glob.glob("/Users/imaik/Documents/SHW-Readerv2/SHW-Reader/translations/*.json")
    for file_path in translation_files:
        if 'config.json' in file_path:
            continue
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        changed = False
        if 'menu' in data:
            menu = data['menu']
            for key in ['export_excel', 'export_word']:
                if key in menu:
                    del menu[key]
                    changed = True
        if changed:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✅ Limpiado: {os.path.basename(file_path)}")
        else:
            print(f"Sin cambios: {os.path.basename(file_path)}")

if __name__ == "__main__":
    clean_menu_translations()
    print("🧹 Limpieza de menú completada.")
