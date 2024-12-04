import os
import pandas as pd
from process2 import AbstractAPI
from datetime import datetime
from dateutil.relativedelta import relativedelta


class Microservice_2(AbstractAPI):
    def data_parameters(self):
        now = datetime.now()
        monthLast = now - relativedelta(months=1)
        previousMonth = monthLast.strftime("%B")
        formatDate = monthLast.strftime("%Y-%m")

        # Carpeta relativa donde se guardarán las descargas en el contenedor
        download_dir = "C:\\Users\\usuario\\Downloads"
        # download_dir = os.getenv("DOWNLOAD_DIR", "/downloads")  # Cambia "/app/downloads" a donde quieras que esté en el contenedor
        path_xlsx = f"{previousMonth}Generacion_{formatDate}.xls"

        # Ruta completa del archivo Excel
        file_path = os.path.join(download_dir, path_xlsx)

        # Cargar el archivo Excel
        device_data = pd.read_excel(file_path)

        # Procesamiento de los datos
        device_data.columns = device_data.iloc[0]
        device_data = device_data[1:]
        device_data["Monthly Cumulative Power generation"] = device_data[
            "Monthly Cumulative Power generation"
        ].astype(float)
        Generacion = (
            device_data.groupby("plantName")["Monthly Cumulative Power generation"]
            .sum()
            .reset_index()
        )
        Generacion["fechaFactura"] = formatDate

        # Convertir a JSON
        json_data = Generacion.to_json(orient="records")
        return json_data
