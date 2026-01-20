# ML Patient Data Processing & Automation Tool

An Machine Learning-powered tool i built myself for automating the processing and cleansing of patient data in Excel spreadsheets. Designed to replace manual document review, this software uses machine learning to determine whether an entry should be displayed ("anzeigen") or deleted ("löschen"). Our team saves a lot of time using my tool.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technical Details](#technical-details)
- [Example Workflow](#example-workflow)
- [Changelog](#changelog)
- [Lizenz](#Lizenz)

## Overview

Traditionally, patient data processing in Excel was a manual task where each row had to be reviewed individually. This tool automates that process by training a **Naive Bayes classifier** on historical Excel datasets and applying it to new datasets to predict the appropriate action (**display or delete**).




## Features

✅ **Automated Data Classification** – Uses machine learning to classify each data entry as "display" or "delete" based on economic relevance.

✅ **Text Normalization** – Converts characters like `ae` → `ä`, `oe` → `ö`, `ue` → `ü`, ensuring consistent name processing.

✅ **Excel File Analysis** – Reads and processes Excel files containing patient information.

✅ **User-Friendly GUI** – Provides an intuitive interface for non-technical users.

✅ **Scalability** – Optimized to handle **10,000+ rows** efficiently.

✅ **JSON Data Export** – Processed results can be saved in **JSON format** for integration with other systems.

## Technical Details

The software is structured into two main components:

### **1️⃣ Entry Point**
- `main.py` – Application entry point with GUI launcher.

### **2️⃣ Core Modules (`SRC/` directory)**
- `gui.py` – Graphical user interface for non-technical users.
- `processor.py` – Central processing orchestration.
- `data_loader.py` – Loads patient data from Excel files.
- `training.py` – Trains the model using labeled historical data.
- `predict.py` – Applies the trained Naive Bayes model to classify new data.
- `text_processing.py` – Handles **text normalization** (e.g., `ae` → `ä`).
- `excel_analyser.py` – Analyzes titles and groups similar patient data entries.
- `json_writer.py` – Exports processed results as JSON.
- `pre_settings.py` – Configuration and preprocessing settings.
- `exceptions.py` – Custom exception handling.


## Example Workflow
![grafik](https://github.com/user-attachments/assets/0081cf48-fc0c-4660-8a68-c9652e85576e)


### **Training Phase:**
- The tool is trained using **historically labeled Excel files** (files where the "Operation" column is correctly set to "anzeigen" or "löschen").
- `training.py` processes these files and trains the Naive Bayes model.

### **Prediction Phase:**
- A new Excel file is loaded into the tool.
- The trained model predicts whether each entry should be displayed or deleted.

### **Result Review & Export:**

- Final results can be **saved back to Excel** 

## Changelog

### v2.0.0 (Januar 2026)
- **Projektstruktur überarbeitet** – Alle Module in `SRC/` konsolidiert
- **Neuer Entry Point** – `main.py` im Root-Verzeichnis
- **GUI integriert** – GUI-Modul in Core-Module verschoben
- **Processor-Modul** – Neue zentrale Verarbeitungslogik
- **Exception Handling** – Eigene Exception-Klassen hinzugefügt
- **Dependencies** – `requirements.txt` hinzugefügt

### v1.0.0 (Initial Release)
- Erste Version mit Naive Bayes Klassifikator
- Excel-Verarbeitung und Text-Normalisierung
- Grundlegende GUI

## Lizenz

Der Quellcode dieses Projekts ist **nicht zur Wiederverwendung freigegeben**.
Er darf **ausschließlich zu Demonstrations- und Informationszwecken gelesen**, aber **nicht kopiert, verändert oder verwendet** werden.  

