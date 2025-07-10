#!/usr/bin/env python3
import json
import os

# Nuevas claves que necesitamos agregar
new_keys = {
    "table_sorted": {
        "fr": "Table triée par {column} ({direction})",
        "de": "Tabelle sortiert nach {column} ({direction})",
        "it": "Tabella ordinata per {column} ({direction})",
        "pt": "Tabela ordenada por {column} ({direction})",
        "ca": "Taula ordenada per {column} ({direction})",
        "gl": "Táboa ordenada por {column} ({direction})",
        "eu": "Taula {column}ren arabera ordenatuta ({direction})"
    },
    "ascending": {
        "fr": "croissant",
        "de": "aufsteigend",
        "it": "crescente",
        "pt": "crescente",
        "ca": "ascendent",
        "gl": "ascendente",
        "eu": "gorantz"
    },
    "descending": {
        "fr": "décroissant",
        "de": "absteigend",
        "it": "decrescente",
        "pt": "decrescente",
        "ca": "descendent",
        "gl": "descendente",
        "eu": "beherantz"
    },
    "file_success": {
        "fr": "Fichier \"{filename}\" chargé avec succès. {devices} appareils, {rows} canaux",
        "de": "Datei \"{filename}\" erfolgreich geladen. {devices} Geräte, {rows} Kanäle",
        "it": "File \"{filename}\" caricato con successo. {devices} dispositivi, {rows} canali",
        "pt": "Arquivo \"{filename}\" carregado com sucesso. {devices} dispositivos, {rows} canais",
        "ca": "Fitxer \"{filename}\" carregat correctament. {devices} dispositius, {rows} canals",
        "gl": "Arquivo \"{filename}\" cargado correctamente. {devices} dispositivos, {rows} canais",
        "eu": "\"{filename}\" fitxategia behar bezala kargatu da. {devices} gailu, {rows} kanal"
    },
    "file_error_processing": {
        "fr": "Erreur lors du traitement du fichier",
        "de": "Fehler beim Verarbeiten der Datei",
        "it": "Errore durante l'elaborazione del file",
        "pt": "Erro ao processar o arquivo",
        "ca": "Error en processar el fitxer",
        "gl": "Erro ao procesar o arquivo",
        "eu": "Errorea fitxategia prozesatzean"
    },
    "file_processed": {
        "fr": "Fichier traité: {devices} appareils, {rows} lignes",
        "de": "Datei verarbeitet: {devices} Geräte, {rows} Zeilen",
        "it": "File elaborato: {devices} dispositivi, {rows} righe",
        "pt": "Arquivo processado: {devices} dispositivos, {rows} linhas",
        "ca": "Fitxer processat: {devices} dispositius, {rows} files",
        "gl": "Arquivo procesado: {devices} dispositivos, {rows} filas",
        "eu": "Fitxategia prozesatuta: {devices} gailu, {rows} errenkada"
    },
    "connection_error": {
        "fr": "Erreur de connexion",
        "de": "Verbindungsfehler",
        "it": "Errore di connessione",
        "pt": "Erro de conexão",
        "ca": "Error de connexió",
        "gl": "Erro de conexión",
        "eu": "Konexio errorea"
    },
    "field_updated": {
        "fr": "Champ mis à jour",
        "de": "Feld aktualisiert",
        "it": "Campo aggiornato",
        "pt": "Campo atualizado",
        "ca": "Camp actualitzat",
        "gl": "Campo actualizado",
        "eu": "Eremua eguneratuta"
    },
    "rows_selected": {
        "fr": "{count} ligne(s) sélectionnée(s)",
        "de": "{count} Zeile(n) ausgewählt",
        "it": "{count} riga/righe selezionata/e",
        "pt": "{count} linha(s) selecionada(s)",
        "ca": "{count} fila/files seleccionada/es",
        "gl": "{count} fila(s) seleccionada(s)",
        "eu": "{count} errenkada hautatuta"
    },
    "no_na_channels": {
        "fr": "Aucune ligne avec le nom de canal \"N/A\" trouvée à supprimer",
        "de": "Keine Zeilen mit Kanalname \"N/A\" zum Löschen gefunden",
        "it": "Nessuna riga con nome canale \"N/A\" trovata da eliminare",
        "pt": "Nenhuma linha com nome de canal \"N/A\" encontrada para deletar",
        "ca": "No s'han trobat files amb nom de canal \"N/A\" per eliminar",
        "gl": "Non se atoparon filas con nome de canal \"N/A\" para eliminar",
        "eu": "Ez da aurkitu \"N/A\" kanal izeneko errenkadarik ezabatzeko"
    },
    "invalid_file": {
        "fr": "Seuls les fichiers .shw sont autorisés",
        "de": "Nur .shw-Dateien sind erlaubt",
        "it": "Solo i file .shw sono consentiti",
        "pt": "Apenas arquivos .shw são permitidos",
        "ca": "Només es permeten fitxers .shw",
        "gl": "Só se permiten arquivos .shw",
        "eu": ".shw fitxategiak bakarrik onartzen dira"
    }
}

# Actualizar cada archivo de traducción
for lang in ['fr', 'de', 'it', 'pt', 'ca', 'gl', 'eu']:
    file_path = f'/Users/imaik/Documents/WWB to Excel/translations/{lang}.json'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Agregar las nuevas claves
        for key, translations in new_keys.items():
            if lang in translations:
                data['messages'][key] = translations[lang]
        
        # También actualizar invalid_file para que coincida con la nueva versión
        if 'invalid_file' in data['messages']:
            data['messages']['invalid_file'] = new_keys['invalid_file'][lang]
        
        # Guardar el archivo actualizado
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Actualizado {lang}.json")
    
    except Exception as e:
        print(f"❌ Error actualizando {lang}.json: {e}")

print("🎉 Actualización de traducciones completada")
