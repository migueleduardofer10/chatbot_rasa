import os
import pandas as pd
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionProveerDemografia(Action):

    def name(self) -> Text:
        return "action_proveer_demografia"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Imprimir el directorio de trabajo actual
        print("Directorio de trabajo actual:", os.getcwd())

        # Determinar la ruta absoluta del archivo CSV
        current_dir = os.getcwd()
        csv_path = os.path.join(current_dir, 'actions', 'indicadores_demograficos.csv')
        print("Ruta del archivo CSV:", csv_path)

        # Verificar si el archivo existe
        if not os.path.exists(csv_path):
            dispatcher.utter_message(text=f"Archivo no encontrado: {csv_path}")
            print("Archivo no encontrado:", csv_path)
            return []

        # Cargar los datos del archivo CSV con el delimitador correcto
        try:
            data = pd.read_csv(csv_path, delimiter=',', encoding='utf-8')
            print("Archivo CSV cargado correctamente.")
        except Exception as e:
            dispatcher.utter_message(text=f"Error al leer el archivo CSV: {str(e)}")
            print("Error al leer el archivo CSV:", str(e))
            return []

        # Imprimir las primeras filas y los nombres de las columnas del DataFrame
        print("Nombres de las columnas:", data.columns)
        print("Primeras filas del DataFrame:\n", data.head())

        # Obtener el nombre del país
        pais = next(tracker.get_latest_entity_values("pais"), None)
        print("Entidad 'pais' recibida:", pais)

        if not pais:
            dispatcher.utter_message(text="Por favor, especifique un país.")
            print("No se proporcionó un país.")
            return []

        # Buscar datos del país
        try:
            datos_pais = data[data['País'].str.contains(pais, case=False, na=False)]
            print("Datos del país encontrados:\n", datos_pais)
        except KeyError as e:
            dispatcher.utter_message(text=f"Error de clave: {e}")
            print("Error de clave:", str(e))
            return []

        if datos_pais.empty:
            dispatcher.utter_message(text=f"No se encontraron datos para {pais}.")
            print(f"No se encontraron datos para {pais}.")
        else:
            respuesta = datos_pais.to_string(index=False)
            dispatcher.utter_message(text=respuesta)
            print("Respuesta enviada:\n", respuesta)

        return []
