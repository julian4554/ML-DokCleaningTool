"""
JSON-Writer-Modul für das ML-DokCleaningTool.

Dieses Modul enthält Funktionen zum Schreiben von Analyseergebnissen
in JSON-Dateien.
"""

import json


def write_results_to_json(results, output_file):
    """
    Schreibt die Analyseergebnisse in eine JSON-Datei.

    Args:
        results (dict): Die Analyseergebnisse, die geschrieben werden sollen.
        output_file (str): Der Pfad zur Ausgabe-JSON-Datei.
    """
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False, indent=4)
