"""
Excel-Analyse-Modul für das ML-DokCleaningTool.

Dieses Modul enthält Funktionen zur Analyse von Excel-Dokumentlisten
und zur Zusammenfassung von Titeln.
"""

import json
import os

import pandas as pd

from src.json_writer import write_results_to_json

# Standard-Ausgabedatei
OUTPUT_FILE = os.path.join(os.path.expanduser('~'), 'ergebnisse.json')


def summarize_titles(file_path, column_name='Titel', origin_column='Herkunft', min_count=5):
    data = pd.read_excel(file_path)
    titles = data[column_name].tolist()
    origins = data[origin_column].tolist()
    summarized_titles = {}
    current_prefix = None
    current_count = 0
    current_titles = []
    current_origins = []

    for title, origin in zip(titles, origins):
        if pd.isna(title):
            continue
        prefix = title.split()[0]
        if prefix == current_prefix:
            current_count += 1
            if title not in current_titles:
                current_titles.append(title)
            if origin not in current_origins:
                current_origins.append(origin)
        else:
            if current_count >= min_count:
                if len(current_titles) == 1:
                    summarized_titles[current_titles[0]] = current_origins
                else:
                    summarized_titles[f"{current_prefix}.*"] = current_origins
            current_prefix = prefix
            current_count = 1
            current_titles = [title]
            current_origins = [origin]

    # Check the last group
    if current_count >= min_count:
        if len(current_titles) == 1:
            summarized_titles[current_titles[0]] = current_origins
        else:
            summarized_titles[f"{current_prefix}.*"] = current_origins

    # Remove duplicates from JSON
    summarized_titles = {k: list(set(v)) for k, v in summarized_titles.items()}

    return json.dumps(summarized_titles, ensure_ascii=False)


def analyze_dok_listen(file_path):
    """
    Hauptfunktion zur Analyse von Dokumentlisten.

    Analysiert eine Excel-Datei und schreibt die zusammengefassten
    Ergebnisse in eine JSON-Datei.

    Args:
        file_path (str): Pfad zur Excel-Datei.
    """
    results = summarize_titles(file_path)
    results_dict = json.loads(results)
    write_results_to_json(results_dict, OUTPUT_FILE)
