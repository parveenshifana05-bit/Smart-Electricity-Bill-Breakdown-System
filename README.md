# Smart Electricity Bill Breakdown System

## Project Overview
The Smart Electricity Bill Breakdown System is a Python-based desktop application developed to help users understand and analyse their electricity consumption.

The application reads meter readings from a CSV file, validates the data, calculates electricity consumption and estimates the electricity bill. It also provides appliance-level analysis, usage alerts, energy-saving suggestions and reports.

## Technologies Used
- Python
- Tkinter
- Pandas
- Matplotlib
- SQLite

## Features
- CSV meter data import and validation
- Electricity consumption calculation
- Slab-based estimated bill calculation
- SQLite database storage
- Daily usage analytics and graphs
- Appliance consumption analysis
- High-usage detection
- Energy-saving suggestions
- Electricity usage notifications
- Report generation
- Graphical user interface

## Project Modules
| File | Description |
|---|---|
| main.py | Main program |
| csv_import.py | Reads and validates CSV data |
| database.py | Handles SQLite operations |
| bill_calculation.py | Calculates estimated bills |
| analytics.py | Calculates usage statistics |
| appliance.py | Appliance consumption calculations |
| waste_detection.py | Detects high appliance usage |
| notifications.py | Displays usage notifications |
| reports.py | Generates electricity reports |
| dashboard.py | Provides the Tkinter interface |

## Requirements
- Python 3
- Pandas
- Matplotlib
- Tkinter
- SQLite

## How to Run
1. Install Python 3.
2. Install the required libraries using:

   pip install -r requirements.txt

3. Open the project folder in VS Code.
4. Run the following command in the terminal:

   python main.py

## Input Data
The application uses meter_data.csv as sample meter-reading input.

## Database
The application uses SQLite to store meter readings, user information, appliance details and bill records.

## Note
The electricity tariff values are prototype rates used for demonstration. The CSV input simulates meter readings; the application is not connected to a physical smart meter.