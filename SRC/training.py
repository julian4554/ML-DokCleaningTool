"""
Training-Modul für das ML-DokCleaningTool.

Dieses Modul enthält Funktionen zum Laden und Vorbereiten von Trainingsdaten,
zum Trainieren des Multinomial Naive Bayes Klassifikationsmodells
und zur Evaluation der Modellgenauigkeit.

Neu: Model-Caching mit joblib für schnelleren Anwendungsstart.
"""

import logging
import os
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.naive_bayes import MultinomialNB

# Pfad für gecachte Modelle
MODEL_CACHE_DIR = Path(__file__).parent.parent / "models"
MODEL_FILE = MODEL_CACHE_DIR / "classifier_model.joblib"
VECTORIZER_FILE = MODEL_CACHE_DIR / "vectorizer.joblib"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def load_and_prepare_data(folder_name):
    """
    Loads data from the Excel files in the specified folder and prepares it for training.

    Args:
        folder_name (str): The path to the folder containing the Excel files.
    Returns:
        tuple: A tuple consisting of two lists, all_X and all_y.
               all_X contains all text data from the Excel files.
               all_y contains all corresponding labels.
    """
    all_X = []
    all_y = []

    for filename in os.listdir(folder_name):
        if filename.endswith(".xlsx"):
            file_path = os.path.join(folder_name, filename)
            try:
                df = pd.read_excel(file_path)
                logging.info(f"Successfully read {file_path}")
            except Exception as e:
                logging.error(f"Error reading {file_path}: {e}")
                continue

            # Check if the necessary columns exist
            if 'TitelDB' in df.columns and 'Beispiel' in df.columns and 'Operation' in df.columns:
                # Ensure specific columns are of type string before filling NaN values
                df['TitelDB'] = df['TitelDB'].astype(str)
                df['Beispiel'] = df['Beispiel'].astype(str)

                # Fill NaN values appropriately
                for column in df.columns:
                    if df[column].dtype == 'object':
                        df[column] = df[column].fillna('')
                    elif df[column].dtype in ['int64', 'float64']:
                        df[column] = df[column].fillna(0)

                # Prepare data for training
                X = df['TitelDB'] + ' ' + df['Beispiel']
                y = df['Operation']

                all_X.extend(X)
                all_y.extend(y)
            else:
                logging.warning(f"Missing columns in {file_path}")
                continue

    return all_X, all_y


def train_model(all_X, all_y):
    """
    Trains a classification model on the provided data.

    Args:
        all_X (list): A list of text data.
        all_y (list): A list of corresponding labels.
    Returns:
        tuple: A tuple consisting of the trained model and the vectorizer.
               The trained model can be used to make predictions,
               and the vectorizer has been fitted to the training data and can
               be used to transform new text data.
    """
    vectorizer = CountVectorizer()
    X_all_vec = vectorizer.fit_transform(all_X)

    model = MultinomialNB()

    # Parameter tuning using GridSearchCV
    param_grid = {
        'alpha': [0.1, 0.5, 1.0]
    }
    grid_search = GridSearchCV(model, param_grid, cv=5)
    grid_search.fit(X_all_vec, all_y)

    best_model = grid_search.best_estimator_

    logging.info("Model training complete. Best parameters: %s", grid_search.best_params_)

    return best_model, vectorizer


def evaluate_model(model, vectorizer, all_X, all_y):
    """
    Evaluates the trained model on a test set and logs the accuracy.

    Args:
        model: The trained model.
        vectorizer: The fitted vectorizer.
        all_X (list): A list of text data.
        all_y (list): A list of corresponding labels.
    """
    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(all_X, all_y, test_size=0.2, random_state=42)

    # Transform the test data using the fitted vectorizer
    X_test_vec = vectorizer.transform(X_test)

    # Make predictions on the test data
    y_pred = model.predict(X_test_vec)

    # Calculate the accuracy of the model
    accuracy = accuracy_score(y_test, y_pred)
    logging.info(f"Model accuracy: {accuracy * 100:.2f}%")


def save_model(model, vectorizer):
    """
    Speichert das trainierte Modell und den Vectorizer auf der Festplatte.

    Args:
        model: Das trainierte Klassifikationsmodell.
        vectorizer: Der gefittete CountVectorizer.

    Returns:
        bool: True wenn erfolgreich gespeichert, False bei Fehler.
    """
    try:
        MODEL_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, MODEL_FILE)
        joblib.dump(vectorizer, VECTORIZER_FILE)
        logging.info(f"Modell gespeichert in {MODEL_CACHE_DIR}")
        return True
    except Exception as e:
        logging.error(f"Fehler beim Speichern des Modells: {e}")
        return False


def load_model():
    """
    Lädt ein zuvor gespeichertes Modell und Vectorizer von der Festplatte.

    Returns:
        tuple: (model, vectorizer) wenn erfolgreich, (None, None) wenn nicht vorhanden.
    """
    if MODEL_FILE.exists() and VECTORIZER_FILE.exists():
        try:
            model = joblib.load(MODEL_FILE)
            vectorizer = joblib.load(VECTORIZER_FILE)
            logging.info("Gecachtes Modell erfolgreich geladen")
            return model, vectorizer
        except Exception as e:
            logging.warning(f"Fehler beim Laden des gecachten Modells: {e}")
            return None, None
    return None, None


def get_model(training_data_folder):
    """
    Holt das Modell - entweder aus dem Cache oder trainiert neu.

    Diese Funktion prüft zuerst, ob ein gecachtes Modell existiert.
    Falls ja, wird dieses geladen. Falls nein, wird ein neues Modell
    trainiert und für zukünftige Verwendung gespeichert.

    Args:
        training_data_folder (str): Pfad zum Ordner mit Trainingsdaten.

    Returns:
        tuple: (model, vectorizer) - Das Klassifikationsmodell und der Vectorizer.
    """
    # Versuche gecachtes Modell zu laden
    model, vectorizer = load_model()
    if model is not None and vectorizer is not None:
        return model, vectorizer

    # Kein Cache vorhanden - neu trainieren
    logging.info("Kein gecachtes Modell gefunden, starte Training...")
    all_X, all_y = load_and_prepare_data(training_data_folder)

    if not all_X or not all_y:
        raise ValueError("Keine Trainingsdaten gefunden")

    model, vectorizer = train_model(all_X, all_y)

    # Modell für nächsten Start cachen
    save_model(model, vectorizer)

    return model, vectorizer



