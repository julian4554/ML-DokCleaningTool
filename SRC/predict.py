"""
Vorhersage-Modul für das ML-DokCleaningTool.

Dieses Modul enthält Funktionen zur Vorhersage von Klassifikationen
für neue Dokumente unter Verwendung des trainierten Modells.
"""

import logging

import pandas as pd

from src.text_processing import adjust_text
from src.pre_settings import apply_pre_settings


logger = logging.getLogger(__name__)

def predict_new_data(new_data_path, model, vectorizer):
    """
    Makes predictions for new data using the trained model and vectorizer.

    Args:
        new_data_path (str): The path to the file containing the new data.
        model: The trained classification model.
        vectorizer: The trained vectorizer.
    Returns:
        pandas.DataFrame: A DataFrame with the predicted labels for the new data.
    """
    try:
        # Load new data
        df_new_data = pd.read_excel(new_data_path)
    except Exception as e:
        logger.error(f"Failed to load new data: {e}")
        raise

    # Ensure specific columns are of type string
    for col in ['TitelAnzeige', 'TitelDB', 'Beispiel']:
        if col in df_new_data:
            df_new_data[col] = df_new_data[col].astype(str)
        else:
            logger.warning(f"Column {col} not found in the data")

    # Fill NaN values appropriately
    for column in df_new_data.columns:
        if df_new_data[column].dtype == 'object':
            df_new_data[column] = df_new_data[column].fillna('')
        elif df_new_data[column].dtype in ['int64', 'float64']:
            df_new_data[column] = df_new_data[column].fillna(0)

    # Apply text processing and pre-settings
    df_new_data['TitelAnzeige'] = df_new_data['TitelAnzeige'].apply(adjust_text)
    df_new_data = apply_pre_settings(df_new_data)

    # Prepare data
    X_new_data = df_new_data[['TitelDB', 'Beispiel']].astype(str)

    # Vectorize text
    try:
        X_new_data_vec = vectorizer.transform(X_new_data['TitelDB'] + ' ' + X_new_data['Beispiel'])
    except Exception as e:
        logger.error(f"Failed to vectorize new data: {e}")
        raise

    # Make predictions for new data
    try:
        predictions_new_data = model.predict(X_new_data_vec)
    except Exception as e:
        logger.error(f"Model prediction failed: {e}")
        raise

    # Add the predictions of the new data into the 'Operation' column of the new table
    df_new_data['Operation'] = predictions_new_data

    return df_new_data
