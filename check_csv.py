import pandas as pd

# Ruta al archivo CSV
csv_path = 'C:\\Users\\Miguel\\OneDrive\\Documentos\\chatbot_si\\actions\\demographic_indicators.csv'

# Cargar los datos del archivo CSV con el delimitador correcto
try:
    data = pd.read_csv(csv_path, delimiter=',', encoding='utf-8')
    print("Column names:", data.columns)
    print("First few rows of the DataFrame:\n", data.head())
except Exception as e:
    print(f"Error reading CSV file: {str(e)}")
