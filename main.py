"""
ML-DokCleaningTool - Haupteinstiegspunkt.

Startet die grafische Benutzeroberfläche für die automatisierte
Dokumentenklassifikation und -bereinigung.

Verwendung:
    python main.py
"""

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

from src.gui import AnalyzerGUI, SplashScreen


def main():
    """Startet die Anwendung mit Splash-Screen und Hauptfenster."""
    app = QApplication(sys.argv)

    # Splash-Screen anzeigen
    splash = SplashScreen()
    splash.show()
    app.processEvents()

    # Hauptfenster erstellen
    main_window = AnalyzerGUI()

    # Nach 3 Sekunden: Splash schließen und Hauptfenster zeigen
    QTimer.singleShot(3000, splash.close)
    QTimer.singleShot(3000, main_window.show)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
