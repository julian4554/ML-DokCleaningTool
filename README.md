# ML Patient Data Processing & Automation Tool

An Machine Learning-powered tool i built myself for automating the processing and cleansing of patient data in Excel spreadsheets. Designed to replace manual document review, this software uses machine learning to determine whether an entry should be displayed ("anzeigen") or deleted ("löschen"). Our team saves a lot of time using my tool.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technical Details](#technical-details)
- [Example Workflow](#example-workflow)
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

The software is structured into three main components:

### **1️⃣ GUI** (Graphical User Interface)
![image](https://github.com/user-attachments/assets/493a2868-0ed0-430a-bb44-6163addf3f83)

- Located in the `GUI/` directory.
- Includes `main_gui.py` for launching the user interface.
- Uses custom icons (`.ico`, `.jpg`).

### **2️⃣ Core Processing (`src/` directory)**
- `main.py` – Central control module.
- `data_loader.py` – Loads patient data from Excel files.
- `training.py` – Trains the model using labeled historical data.
- `predict.py` – Applies the trained Naive Bayes model to classify new data.
- `text_processing.py` – Handles **text normalization** (e.g., `ae` → `ä`).

### **3️⃣ Additional Processing (`srcDokListen/` directory)**
- `excel_analyser.py` – Analyzes titles and groups similar patient data entries.
- `json_writer.py` – Enables better readability for subtasks as JSON.


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

## Lizenz

Der Quellcode dieses Projekts ist **nicht zur Wiederverwendung freigegeben**.  
Er darf **ausschließlich zu Demonstrations- und Informationszwecken gelesen**, aber **nicht kopiert, verändert oder verwendet** werden.  

