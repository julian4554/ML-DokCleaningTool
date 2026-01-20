"""
Exceptions-Modul für das ML-DokCleaningTool.

Dieses Modul enthält benutzerdefinierte Exceptions für eine
strukturierte Fehlerbehandlung mit benutzerfreundlichen Meldungen.
"""


class ProcessingError(Exception):
    """
    Fehler bei der Dokumentenverarbeitung.

    Diese Exception wird geworfen, wenn bei der Verarbeitung von
    Dokumenten ein Fehler auftritt, der dem Benutzer mitgeteilt
    werden soll.

    Attributes:
        message (str): Benutzerfreundliche Fehlerbeschreibung.
        original_error (Exception): Die ursprüngliche Exception, falls vorhanden.
    """

    def __init__(self, message: str, original_error: Exception = None):
        """
        Initialisiert die ProcessingError Exception.

        Args:
            message (str): Benutzerfreundliche Fehlerbeschreibung.
            original_error (Exception): Die ursprüngliche Exception.
        """
        self.message = message
        self.original_error = original_error
        super().__init__(self.message)

    def __str__(self):
        return self.message


class FileLoadError(ProcessingError):
    """Fehler beim Laden einer Datei."""
    pass


class ModelError(ProcessingError):
    """Fehler beim Laden oder Trainieren des ML-Modells."""
    pass


class ClassificationError(ProcessingError):
    """Fehler bei der Klassifikation von Dokumenten."""
    pass
