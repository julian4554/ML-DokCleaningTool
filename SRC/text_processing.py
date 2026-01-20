"""
Text-Processing-Modul für das ML-DokCleaningTool.

Dieses Modul enthält Funktionen zur Textvorverarbeitung und -bereinigung,
einschließlich Umlaut-Ersetzung und Textformatierung.
"""

import re


def adjust_text(text):
    """
    Performs all specific text adjustments.

    Args:
        text (str): The text to be adjusted.
    Returns:
        str: The adjusted text.
    """

    if text is None or text == "nan" or text == "":  # Check if the text is None, "nan", or empty
        return ""

    umlauts = {
        'ae': 'ä',
        'oe': 'ö',
        'ue': 'ü',
        'Ae': 'Ä',
        'Oe': 'Ö',
        'Ue': 'Ü',
        'sz': 'ß'
    }
    for replacement, umlaut in umlauts.items():
        text = text.replace(replacement, umlaut)

    text = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', text)
    text = re.sub(r'\bTXT\b|\btxt\b', '', text, flags=re.IGNORECASE)
    text = text.replace('gepl', 'geplant')
    return text
