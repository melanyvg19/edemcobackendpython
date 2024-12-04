# Importamos las bibliotecas necesarias
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json

# Definimos la clase Microservice_2 que hereda de AbstractAPI
class Microservice():
    # Definimos el método data_parameters
    def execute(self, file):
        # Leemos el archivo Excel
        device_data = pd.read_excel(file)
        #extraer valor celda p1
        formatDate = pd.to_datetime(device_data.iloc[0, 15]).strftime('%Y-%m')
        # Asignamos los nombres de las columnas del DataFrame
        device_data.columns = device_data.iloc[0]
        # Eliminamos la primera fila del DataFrame
        device_data = device_data[1:]
        # Convertimos la columna 'Monthly Cumulative Power generation' a float
        device_data['Monthly Cumulative Power generation'] = device_data['Monthly Cumulative Power generation'].astype(float)
        # Agrupamos los datos por 'plantName' y sumamos la generación de energía mensual acumulada
        Generacion = device_data.groupby('plantName')['Monthly Cumulative Power generation'].sum().reset_index()
        # Añadimos una nueva columna 'fechaFactura' con la fecha formateada
        Generacion['fechaFactura'] = formatDate
        # Convertimos el DataFrame a JSON
        json_data = Generacion.to_json(orient='records')
        # Devolvemos los datos en formato JSON
        data = json.loads(json_data)

        return data