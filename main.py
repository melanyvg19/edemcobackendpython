import subprocess
import time
import os
import shutil
from config_macros import ConfigMacros

microservices = [
    "microservice_get-invoices/main.py",
    "microservice_growatt-generation/main.py",
    "microservice_historic-factories/main.py",
    "microservice_template-facturas/main.py",
    "microservice_upload-file/main.py",
]


# Función para iniciar cada microservicio
def start_microservice(path):
    return subprocess.Popen(["python", path])


ruta_excel_relativa = os.path.dirname(__file__)
ruta_excel = os.path.join(ruta_excel_relativa, "..", "edemco-facturas")

appdata_path = os.getenv("APPDATA")

# Especificar la ruta relativa dentro de AppData
carpeta_macro = "EdemcoInvoices\\macro_factura"
carpeta_pdf = "EdemcoInvoices\\pdf_factura"

# Construir la ruta completa
ruta_macro = os.path.join(appdata_path, carpeta_macro)
ruta_pdf = os.path.join(appdata_path, carpeta_pdf)

# Verificar si las carpetas existen y crearlas si es necesario
if not os.path.exists(ruta_macro):
    os.makedirs(ruta_macro)
    # Copiar archivos .xlsm al directorio APPDATA
    for file_name in os.listdir(ruta_excel):
        if file_name.endswith(".xlsm"):
            full_file_name = os.path.join(ruta_excel, file_name)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, ruta_macro)
                ruta_config_macro = os.path.join(ruta_macro, file_name)
                ConfigMacros.ejecutar(ruta_config_macro, file_name, ruta_pdf)
    if not os.path.exists(ruta_pdf):
        os.makedirs(ruta_pdf)


# Diccionario para almacenar los procesos y sus respectivas rutas
processes = {path: start_microservice(path) for path in microservices}

# Tiempo de espera entre chequeos de estado (en segundos)
check_interval = 5

try:
    while True:
        for path, process in list(processes.items()):
            # Verifica si el proceso ha terminado
            if process.poll() is not None:  # El proceso ha terminado
                print(f"Microservicio {path} ha fallado. Reiniciando...")
                processes[path] = start_microservice(path)
        time.sleep(check_interval)
except KeyboardInterrupt:
    # Termina todos los procesos al salir del script
    for process in processes.values():
        process.terminate()
    print("Terminando todos los microservicios.")
