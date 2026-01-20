"""
ML-DokCleaningTool - Source Package

Dieses Paket enthält die Kernfunktionalität für die automatisierte
Dokumentenklassifikation und -bereinigung.

Module:
    - processor: Kernverarbeitungslogik (zentrale Schnittstelle)
    - training: ML-Modell Training und Evaluation
    - predict: Vorhersagen für neue Daten
    - text_processing: Textvorverarbeitung und -bereinigung
    - pre_settings: Regelbasierte Vorfilterung
    - data_loader: Daten laden und speichern
    - gui: PyQt5-Benutzeroberfläche (nur GUI-Code)
    - excel_analyser: Excel-Dokumentanalyse
    - json_writer: JSON-Ausgabe
    - exceptions: Benutzerdefinierte Exceptions
"""

from src.processor import process_file, process_dok_listen, validate_file_path
from src.exceptions import ProcessingError, FileLoadError, ModelError, ClassificationError
from src.training import (
    train_model, load_and_prepare_data, evaluate_model,
    save_model, load_model, get_model, MODEL_CACHE_DIR
)
from src.predict import predict_new_data
from src.text_processing import adjust_text
from src.pre_settings import apply_pre_settings
from src.data_loader import save_processed_data, TRAINING_DATA_DIR, PROCESSED_DATA_DIR
from src.excel_analyser import summarize_titles, analyze_dok_listen
from src.json_writer import write_results_to_json

__all__ = [
    # Core Processing
    'process_file',
    'process_dok_listen',
    'validate_file_path',
    # Exceptions
    'ProcessingError',
    'FileLoadError',
    'ModelError',
    'ClassificationError',
    # Training & Model Caching
    'train_model',
    'load_and_prepare_data',
    'evaluate_model',
    'save_model',
    'load_model',
    'get_model',
    'MODEL_CACHE_DIR',
    # Prediction
    'predict_new_data',
    # Text Processing
    'adjust_text',
    'apply_pre_settings',
    # Data Management
    'save_processed_data',
    'TRAINING_DATA_DIR',
    'PROCESSED_DATA_DIR',
    # Excel Analysis
    'summarize_titles',
    'analyze_dok_listen',
    'write_results_to_json',
]
