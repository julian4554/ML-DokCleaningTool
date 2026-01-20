"""
Processor-Modul für das ML-DokCleaningTool.

Dieses Modul enthält die Kernverarbeitungslogik für die
Dokumentenklassifikation und -verarbeitung. Es dient als
zentrale Schnittstelle zwischen GUI und Business-Logik.
"""

import logging
import os
import tempfile

from src.data_loader import save_processed_data, TRAINING_DATA_DIR
from src.exceptions import ProcessingError, FileLoadError, ModelError, ClassificationError
from src.training import get_model
from src.predict import predict_new_data
from src.excel_analyser import summarize_titles
from src.json_writer import write_results_to_json

import json

logger = logging.getLogger(__name__)


def validate_file_path(file_path: str) -> None:
    """
    Validiert einen Dateipfad auf Existenz und Lesbarkeit.

    Args:
        file_path (str): Der zu validierende Dateipfad.

    Raises:
        FileLoadError: Wenn die Datei nicht existiert oder nicht lesbar ist.
    """
    if not file_path:
        raise FileLoadError("Kein Dateipfad angegeben.")

    if not os.path.exists(file_path):
        raise FileLoadError(f"Datei nicht gefunden: {file_path}")

    if not os.path.isfile(file_path):
        raise FileLoadError(f"Pfad ist keine Datei: {file_path}")

    if not os.access(file_path, os.R_OK):
        raise FileLoadError(f"Keine Leseberechtigung für: {file_path}")

    # Prüfe auf gültige Excel-Endung
    valid_extensions = ('.xlsx', '.xls')
    if not file_path.lower().endswith(valid_extensions):
        raise FileLoadError(
            f"Ungültiges Dateiformat. Erlaubt sind: {', '.join(valid_extensions)}"
        )


def process_file(file_path: str, gui=None) -> str:
    """
    Verarbeitet eine Datei mit dem ML-Klassifikationsmodell.

    Lädt das Modell aus dem Cache oder trainiert neu,
    macht Vorhersagen und speichert die verarbeiteten Daten.

    Args:
        file_path (str): Pfad zur Eingabedatei.
        gui: Optionale GUI-Instanz für Progress-Updates.

    Returns:
        str: Pfad zur verarbeiteten Ausgabedatei.

    Raises:
        FileLoadError: Wenn die Eingabedatei nicht geladen werden kann.
        ModelError: Wenn das Modell nicht geladen/trainiert werden kann.
        ClassificationError: Wenn die Klassifikation fehlschlägt.
    """
    # Dateipfad validieren
    validate_file_path(file_path)

    # Modell laden
    try:
        if gui:
            gui.progress_callback(20)
        logger.info("Lade Modell (Cache oder Training)...")
        model, vectorizer = get_model(TRAINING_DATA_DIR)
        logger.info("Modell bereit für Vorhersagen.")
    except ValueError as e:
        raise ModelError(f"Keine Trainingsdaten gefunden: {e}", e)
    except Exception as e:
        raise ModelError(f"Fehler beim Laden des Modells: {e}", e)

    # Vorhersagen durchführen
    try:
        if gui:
            gui.progress_callback(50)
        logger.info("Führe Klassifikation durch...")
        df_predictions = predict_new_data(file_path, model, vectorizer)
    except KeyError as e:
        raise ClassificationError(
            f"Erforderliche Spalte fehlt in der Datei: {e}", e
        )
    except Exception as e:
        raise ClassificationError(f"Fehler bei der Klassifikation: {e}", e)

    # Ergebnisse speichern
    try:
        if gui:
            gui.progress_callback(80)
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix='.xlsx',
            mode='w',
            encoding='utf-8',
            newline='',
            dir=TRAINING_DATA_DIR
        ) as tmpfile:
            output_path = tmpfile.name
            logger.info(f"Speichere Ergebnisse in {output_path}.")
            save_processed_data(df_predictions, output_path)

        if gui:
            gui.progress_callback(100)
        return output_path

    except Exception as e:
        raise ProcessingError(f"Fehler beim Speichern der Ergebnisse: {e}", e)


def process_dok_listen(file_path: str, output_file: str) -> dict:
    """
    Analysiert eine Dokumentliste und erzeugt zusammengefasste Ergebnisse.

    Diese Funktion extrahiert und gruppiert Dokumenttitel aus einer
    Excel-Datei und schreibt die Ergebnisse in eine JSON-Datei.

    Args:
        file_path (str): Pfad zur Excel-Eingabedatei.
        output_file (str): Pfad für die JSON-Ausgabedatei.

    Returns:
        dict: Die analysierten Ergebnisse als Dictionary.

    Raises:
        FileLoadError: Wenn die Eingabedatei nicht geladen werden kann.
        ProcessingError: Wenn die Analyse fehlschlägt.
    """
    # Dateipfad validieren
    validate_file_path(file_path)

    try:
        logger.info(f"Analysiere Dokumentliste: {file_path}")
        results = summarize_titles(file_path)
        results_dict = json.loads(results)

        # Ergebnisse in JSON schreiben
        write_results_to_json(results_dict, output_file)
        logger.info(f"Ergebnisse gespeichert in: {output_file}")

        return results_dict

    except KeyError as e:
        raise ProcessingError(
            f"Erforderliche Spalte fehlt in der Datei (erwartet: 'Titel', 'Herkunft'): {e}", e
        )
    except json.JSONDecodeError as e:
        raise ProcessingError(f"Fehler bei der JSON-Verarbeitung: {e}", e)
    except Exception as e:
        raise ProcessingError(f"Fehler bei der Dokumentlisten-Analyse: {e}", e)
