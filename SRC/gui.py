"""
GUI-Modul für das ML-DokCleaningTool.

Dieses Modul enthält ausschließlich die PyQt5-basierte Benutzeroberfläche.
Die Business-Logik wird über das processor-Modul aufgerufen.
"""

import json
import logging
import os
import shutil
import sys

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QFileDialog, QListWidget, QMessageBox, QTextEdit, QLabel,
    QSplashScreen, QProgressBar
)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QTimer

from src.exceptions import ProcessingError, FileLoadError, ModelError, ClassificationError

# Constants
WINDOW_X, WINDOW_Y = 100, 100
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 400
OUTPUT_FILE = os.path.join(os.path.expanduser('~'), 'ergebnisse.json')
LOG_FILE = os.path.join(os.path.expanduser('~'), 'analyzer.log')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)


def get_icon_path(filename):
    """
    Ermittelt den Pfad zu Icon-Dateien.

    Unterstützt sowohl normale Ausführung als auch PyInstaller-Bundles.

    Args:
        filename (str): Name der Icon-Datei.

    Returns:
        str: Vollständiger Pfad zur Icon-Datei.
    """
    if getattr(sys, '_MEIPASS', None):
        base_path = sys._MEIPASS
    else:
        # Im Entwicklungsmodus: Projektverzeichnis verwenden
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, filename)


class SplashScreen(QSplashScreen):
    """Splash-Screen für den Anwendungsstart."""

    def __init__(self):
        """Initialisiert den Splash-Screen mit Icon und Bild."""
        super().__init__()
        icon_path = get_icon_path('assets/ai_excel_analysis_icon.ico')
        self.setWindowIcon(QIcon(icon_path))
        splash_path = get_icon_path('assets/ai_excel_analysis_icon-5.jpg')
        self.setPixmap(QPixmap(splash_path))
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)


class JsonDisplayWindow(QWidget):
    """Fenster zur Anzeige von JSON-Ergebnissen."""

    def __init__(self, json_data):
        """
        Initialisiert das JSON-Anzeigefenster.

        Args:
            json_data (str): Die anzuzeigenden JSON-Daten als String.
        """
        super().__init__()
        self.json_data = json_data
        self.initUI()

    def initUI(self):
        self.setWindowTitle('JSON Display')
        self.setGeometry(400, 400, 400, 300)
        layout = QVBoxLayout()
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.textEdit.setText(self.json_data)
        layout.addWidget(self.textEdit)
        self.setLayout(layout)
        self.applyStyle()

    def applyStyle(self):
        self.setStyleSheet("""
            QTextEdit {
                background-color: #2b2b2b;
                color: #ddd;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
        """)


class AnalyzerGUI(QWidget):
    """Hauptfenster der Anwendung für Dokumentenanalyse."""

    def __init__(self):
        """Initialisiert das Hauptfenster der Anwendung."""
        super().__init__()
        self.json_window = None
        self.analyzedFilePath = ""
        self.temp_files = []
        icon_path = get_icon_path('assets/ai_excel_analysis_icon.ico')
        self.setWindowIcon(QIcon(icon_path))
        self.initUI()

    def closeEvent(self, event):
        try:
            self.cleanup_output_file()
            self.cleanup_temp_files()
        except Exception as e:
            logging.error(f"An error occurred while deleting the file: {e}")
        event.accept()

    def cleanup_output_file(self):
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)
            logging.info(f"File {OUTPUT_FILE} was successfully deleted.")
        else:
            logging.info(f"The file {OUTPUT_FILE} does not exist and could not be deleted.")

    def cleanup_temp_files(self):
        for temp_file in self.temp_files:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                    logging.info(f"Deleted temporary file: {temp_file}")
                except OSError as e:
                    logging.error(f"Error deleting file {temp_file}: {e}")

    def initUI(self):
        self.setWindowTitle('DokBereinigungs Tool')
        self.setGeometry(WINDOW_X, WINDOW_Y, WINDOW_WIDTH, WINDOW_HEIGHT)
        mainLayout = QVBoxLayout()
        layout = QVBoxLayout()

        self.uploadBtn = self.create_button('Upload Excel File', self.uploadFile, layout)
        self.fileList = QListWidget()
        layout.addWidget(self.fileList)

        self.removeFileBtn = self.create_button('Remove Selected File', self.removeFile, layout, enabled=False)
        self.analyzeOrbisBtn = self.create_button('Orbis Absätze Analysieren', self.analyzeOrbis, layout, enabled=False)
        self.analyzeDokBtn = self.create_button('DokListen analysieren [BETA]', self.analyzeDok, layout, enabled=False)
        self.downloadBtn = self.create_button('Download Analyzed File', self.downloadFile, layout, enabled=False)

        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)
        layout.addWidget(self.progressBar)

        self.fileList.itemSelectionChanged.connect(self.onSelectionChanged)
        mainLayout.addLayout(layout)
        bottomLayout = QHBoxLayout()
        bottomLayout.addStretch(1)
        createdByLabel = QLabel('Julian Bick')
        bottomLayout.addWidget(createdByLabel)
        mainLayout.addLayout(bottomLayout)
        self.setLayout(mainLayout)
        self.applyStyle()

    def create_button(self, text, handler, layout, enabled=True):
        button = QPushButton(text)
        button.clicked.connect(handler)
        button.setEnabled(enabled)
        layout.addWidget(button)
        return button

    def applyStyle(self):
        self.setStyleSheet("""
            QPushButton {
                background-color: #5c6bc0;
                color: white;
                border-radius: 15px;
                padding: 10px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #7986cb;
            }
            QPushButton:disabled {
                background-color: #3c4a82;
                color: #ccc;
            }
            QListWidget, QTextEdit {
                border-radius: 5px;
                font-size: 14px;
            }
            QLabel {
                font-size: 12px;
                color: #666;
            }
        """)
        self.setFont(QFont('Arial', 10))

    def updateButtonStates(self):
        has_files = bool(self.fileList.count())
        self.analyzeOrbisBtn.setEnabled(has_files)
        self.analyzeDokBtn.setEnabled(has_files)
        self.removeFileBtn.setEnabled(bool(self.fileList.selectedItems()))

    def onSelectionChanged(self):
        self.updateButtonStates()

    def uploadFile(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '', "Excel files (*.xlsx *.xls)")
        if fname:
            self.fileList.addItem(fname)
            self.updateButtonStates()

    def removeFile(self):
        for item in self.fileList.selectedItems():
            self.fileList.takeItem(self.fileList.row(item))
        self.updateButtonStates()
        self.progress_callback(0)

    def analyzeDok(self):
        """Führt die DokListen-Analyse durch (delegiert an processor)."""
        from src.processor import process_dok_listen

        try:
            file_path = self.fileList.item(0).text()
            results = process_dok_listen(file_path, OUTPUT_FILE)
            self.display_json_result(results)
        except FileLoadError as e:
            self.show_error_message(f"Dateifehler: {e}")
        except ProcessingError as e:
            self.show_error_message(f"Verarbeitungsfehler: {e}")

    def show_error_message(self, message):
        """Zeigt eine benutzerfreundliche Fehlermeldung an."""
        QMessageBox.critical(self, "Fehler", str(message))

    def display_json_result(self, results: dict = None):
        """
        Zeigt die JSON-Ergebnisse in einem separaten Fenster an.

        Args:
            results (dict): Die anzuzeigenden Ergebnisse. Falls None,
                           wird aus OUTPUT_FILE gelesen.
        """
        try:
            if results is None:
                with open(OUTPUT_FILE, 'r', encoding='utf-8') as file:
                    results = json.load(file)

            formatted_json = json.dumps(results, indent=4, ensure_ascii=False)
            self.json_window = JsonDisplayWindow(formatted_json)
            self.json_window.show()
        except Exception as e:
            self.show_error_message(f"Fehler bei der Ergebnisanzeige: {e}")

    def progress_callback(self, value):
        self.progressBar.setValue(value)

    def analyzeOrbis(self):
        """Führt die Orbis-Dokumentenanalyse durch (delegiert an processor)."""
        from src.processor import process_file

        try:
            file_path = self.fileList.item(0).text()
            temp_file_path = process_file(file_path, gui=self)
            logging.info(f"Ergebnis gespeichert in: {temp_file_path}")
            self.analyzedFilePath = temp_file_path
            self.temp_files.append(temp_file_path)
            QMessageBox.information(
                self, "Analyse abgeschlossen",
                "Die Orbis-Analyse wurde erfolgreich durchgeführt."
            )
            self.downloadBtn.setEnabled(True)
        except FileLoadError as e:
            self.progress_callback(0)
            self.show_error_message(f"Dateifehler: {e}")
        except ModelError as e:
            self.progress_callback(0)
            self.show_error_message(f"Modellfehler: {e}")
        except ClassificationError as e:
            self.progress_callback(0)
            self.show_error_message(f"Klassifikationsfehler: {e}")
        except ProcessingError as e:
            self.progress_callback(0)
            self.show_error_message(f"Verarbeitungsfehler: {e}")

    def downloadFile(self):
        if self.analyzedFilePath:
            destination, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Excel files (*.xlsx *.xls)")
            if destination:
                try:
                    shutil.copyfile(self.analyzedFilePath, destination)
                    QMessageBox.information(self, "Download Complete", f"File has been saved to {destination}")
                except Exception as e:
                    self.show_error_message(f"Failed to save file: {e}")
