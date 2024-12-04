import os
import xml.etree.ElementTree as ET
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import subprocess
import time
import logging
from pathlib import Path

# Configurar el registro con codificación UTF-8 y modo sobrescritura
logger = logging.getLogger('registro_facturas')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('microservice_get-invoices/registro_facturas.log', mode='a', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class XMLHandler(FileSystemEventHandler):
    def __init__(self, session):
        self.session = session
        self.counter = 0  # Contador de facturas procesadas

    def process_xml(self, file_path):
        try:
            # Extraer el número de factura del nombre del archivo
            invoice_number = os.path.basename(file_path).replace(".xml", "")

            # Verificar si el número de factura existe en la base de datos
            exists_query = text("""
                SELECT COUNT(*) FROM factura WHERE numero_factura = :invoice_number
            """)
            result = self.session.execute(exists_query, {'invoice_number': invoice_number}).scalar()

            if result > 0:
                tree = ET.parse(file_path)
                root = tree.getroot()

                namespaces = {
                    'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2',
                }

                cufe = None
                fecha_dian = None
                fecha_pago = None
                concepto_facturado = None
                note_counter = 0

                # Extraer CUFE
                for element in root.findall("cbc:UUID", namespaces):
                    cufe = element.text
                    break  # Solo tomamos el primer <cbc:UUID> encontrado

                # Extraer fecha DIAN
                for element in root.findall("cbc:IssueDate", namespaces):
                    fecha_dian = element.text
                    break  # Solo tomamos el primer <cbc:IssueDate> encontrado

                # Extraer fecha de pago
                for element in root.findall("cbc:DueDate", namespaces):
                    fecha_pago = element.text
                    break  # Solo tomamos el primer <cbc:DueDate> encontrado

                # Extraer concepto facturado
                for element in root.findall("cbc:Note", namespaces):
                    concepto_facturado = element.text
                    note_counter += 1
                    if note_counter == 1:
                        break  # Ignoramos el resto después del primer <cbc:Note> encontrado

                if cufe and fecha_dian and fecha_pago and concepto_facturado:
                    self.update_database(invoice_number, cufe, fecha_dian, fecha_pago, concepto_facturado)
                else:
                    logger.info(f"Campos requeridos no encontrados en el archivo: {file_path}")
            else:
                logger.info(f"Factura {invoice_number} no encontrada en la base de datos.")

        except PermissionError as e:
            logger.error(f"PermissionError al intentar abrir el archivo: {e}")
        except Exception as e:
            logger.error(f"Error procesando el archivo XML: {e}")

    def update_database(self, invoice_number, cufe, fecha_dian, fecha_pago, concepto_facturado):
        try:
            query = text("""
                UPDATE factura
                SET cufe = :cufe, fecha_dian = :fecha_dian, fecha_pago = :fecha_pago, concepto_facturado = :concepto_facturado
                WHERE numero_factura = :invoice_number
            """)
            self.session.execute(query, {
                'cufe': cufe,
                'fecha_dian': fecha_dian,
                'fecha_pago': fecha_pago,
                'concepto_facturado': concepto_facturado,
                'invoice_number': invoice_number
            })
            self.session.commit()

            self.counter += 1  # Incrementar contador de facturas procesadas
            logger.info(f"Factura {invoice_number} actualizada con CUFE: {cufe}, fecha_dian: {fecha_dian}, fecha_pago: {fecha_pago}, concepto_facturado: {concepto_facturado}")

            if self.counter >= 1:
                time.sleep(1)
                self.clear_console()
                self.counter = 0  # Restablecer el contador

        except Exception as err:
            logger.error(f"Error: {err}")

    def clear_console(self):
        # Limpiar consola en Windows o Unix
        subprocess.run("cls" if os.name == "nt" else "clear", shell=True)

    def on_created(self, event):
        try:
            if event.is_directory:
                return
            filename = os.path.basename(event.src_path)
        
            if filename.startswith("13001fes") or filename.startswith("13001FES"):
                if filename.endswith(".xml"):
                    self.process_xml(event.src_path)
        except:
            print(f'No se encontro la factura: {filename}')

def find_folder(root_folder, target_folder):
    for path in Path(root_folder).rglob(target_folder):
        if path.is_dir():
            return path
    return None

def main():
    DATABASE_URL = "mssql+pyodbc://temptech:Edemco2024*+@10.255.252.2/edemco?driver=ODBC+Driver+17+for+SQL+Server"

    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    # Busca la carpeta 'CalificacionesCenEnergy' y luego la subcarpeta 'XML'
    root_folder = Path.home()  # Puedes ajustar el directorio raíz si es necesario
    target_folder = "CalificacionesCenEnergy"
    calificaciones_path = find_folder(root_folder, target_folder)

    if calificaciones_path:
        path_to_watch = calificaciones_path / "XML"
        if path_to_watch.exists() and path_to_watch.is_dir():
            event_handler = XMLHandler(session)
            observer = Observer()
            observer.schedule(event_handler, path=str(path_to_watch), recursive=False)
            observer.start()

            logger.info(f"Observador iniciado, vigilando el directorio: {path_to_watch}")

            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
                logger.info("Observador detenido.")
            observer.join()
        else:
            logger.error(f"La carpeta 'XML' no se encuentra dentro de '{calificaciones_path}'")
    else:
        logger.error("No se encontró la carpeta 'CalificacionesCenEnergy' en el directorio raíz.")

if __name__ == "__main__":
    main()
