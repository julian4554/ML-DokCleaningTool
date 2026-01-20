"""
Data-Loader-Modul für das ML-DokCleaningTool.

Dieses Modul enthält Funktionen und Konstanten für das Laden
und Speichern von Daten sowie die Definition der Verzeichnisstruktur.
"""

import logging
import os

import pandas as pd

# Determine the base directory relative to the current script location
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))

# Define other directories relative to BASE_DIR
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "processed")
TRAINING_DATA_DIR = os.path.join(BASE_DIR, "trainingData", "DatensaetzeUebung")

# Ensure directories exist
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
os.makedirs(TRAINING_DATA_DIR, exist_ok=True)

def save_processed_data(df, filename):
    """
    Speichert verarbeitete Daten im 'processed'-Ordner.

    Args:
        df (pandas.DataFrame): The DataFrame to be saved.
        filename (str): The name of the file to save the data as.
    """
    try:
        file_path = os.path.join(PROCESSED_DATA_DIR, filename)
        df.to_excel(file_path, index=False)
        logging.info(f"File saved successfully at {file_path}")
    except Exception as e:
        logging.error(f"An error occurred while saving the file: {e}")
