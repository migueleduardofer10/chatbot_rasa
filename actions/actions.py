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

        # Obtener el nombre del país y el tipo de dato solicitado
        pais = next(tracker.get_latest_entity_values("pais"), None)
        tipo_dato = tracker.get_slot("tipo_dato")

        print("Entidad 'pais' recibida:", pais)
        print("Entidad 'tipo_dato' recibida:", tipo_dato)

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
            # Mapear el tipo de dato a la columna correspondiente
          # Mapear el tipo de dato a la columna correspondiente
            columnas = {
                "población": "Población (Miles)",
                "porcentaje de la población que tiene entre 0 a 14 años": "0 a 14 (%)",
                "porcentaje de la población que tiene entre 15 a 64 años": "15 a 64 (%)",
                "porcentaje de la población que tiene 65 años o más": "65 a más (%)",
                "tasa de fecundidad": "Tasa de fecundidad total",
                "esperanza de vida al nacer de los hombres": "Esperanza de vida al nacer Hombre",
                "esperanza de vida al nacer de las mujeres": "Esperanza de vida al nacer Mujer"
            }
            columna = columnas.get(tipo_dato.lower())

            if columna and columna in datos_pais.columns:
                respuesta = datos_pais[columna].values[0]
                dispatcher.utter_message(text=f"El {tipo_dato} de {pais} es {respuesta}.")
                print(f"El {tipo_dato} de {pais} es {respuesta}.")
            else:
                dispatcher.utter_message(text=f"No se encontró el tipo de dato '{tipo_dato}' para {pais}.")
                print(f"No se encontró el tipo de dato '{tipo_dato}' para {pais}.")

        return []
