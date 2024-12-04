import datetime
import locale
import os


class DTO_email:

    @staticmethod
    def execute(cod_planta):
        # Establecer el locale en español
        locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")

        # Obtener la fecha actual
        fecha_actual = datetime.datetime.now()

        # Obtener el nombre del mes en español y el año
        nombre_mes = fecha_actual.strftime("%B")  # Nombre completo del mes
        anio = fecha_actual.year  # Año

        print(f"Mes: {nombre_mes}, Año: {anio}")

        appdata_path = os.getenv("APPDATA")

        match cod_planta:
            case "506":
                # Ceipa Barranquilla
                asunto = f"Detalle de Consumo de Energia Solar - {nombre_mes}, {anio} - Ceipa Barranquilla"
                ruta = "C:\\Users\\usuario\\Desktop\\pdf_facturas\\CEIPABARRANQUIL_fACTURA.pdf"
                ruta_pdf = os.path.join(appdata_path, ruta)
                return asunto, ruta_pdf

            case "508":
                # Liceo Frances
                asunto = f"Detalle de Consumo de Energia Solar - {nombre_mes}, {anio} - Liceo Frances"
                ruta = "C:\\Users\\usuario\\Desktop\\pdf_facturas\\LICEOFRANCESSFV_fACTURA.pdf"
                ruta_pdf = os.path.join(appdata_path, ruta)
                return asunto, ruta_pdf

            case "514":
                # Incubant
                asunto = f"Detalle de Consumo de Energia Solar - {nombre_mes}, {anio} - Incubant"
                ruta = "C:\\Users\\usuario\\Desktop\\pdf_facturas\\INCUBANSSFV_fACTURA.pdf"
                ruta_pdf = os.path.join(appdata_path, ruta)
                return asunto, ruta_pdf

            case "505":
                # Punto clave
                asunto = f"Detalle de Consumo de Energia Solar - {nombre_mes}, {anio} - Punto clave"
                ruta = "C:\\Users\\usuario\\Desktop\\pdf_facturas\\PUNTOCLAVESSFV_fACTURA.pdf"
                ruta_pdf = os.path.join(appdata_path, ruta)
                return asunto, ruta_pdf

            case "512":
                # Lemont Salon Social
                asunto = f"Detalle de Consumo de Energia Solar - {nombre_mes}, {anio} - Lemont Salon Social"
                ruta = "C:\\Users\\usuario\\Desktop\\pdf_facturas\\LEMONT1SALONSOC_fACTURA.pdf"
                ruta_pdf = os.path.join(appdata_path, ruta)
                return asunto, ruta_pdf

            case "513":
                # Pollocoa
                asunto = f"Detalle de Consumo de Energia Solar - {nombre_mes}, {anio} - Pollocoa"
                ruta = "C:\\Users\\usuario\\Desktop\\pdf_facturas\\POLLOCOASSFV_fACTURA.pdf"
                ruta_pdf = os.path.join(appdata_path, ruta)

                return asunto, ruta_pdf

            case "507":
                # Ceipa Sabaneta
                asunto = f"Detalle de Consumo de Energia Solar - {nombre_mes}, {anio} - Ceipa Sabaneta"
                ruta = "C:\\Users\\usuario\\Desktop\\pdf_facturas\\CEIPASABANETASS_fACTURA.pdf"
                ruta_pdf = os.path.join(appdata_path, ruta)
                return asunto, ruta_pdf

            case "511":
                # lemont Porteria
                asunto = f"Detalle de Consumo de Energia Solar - {nombre_mes}, {anio} - Lemont Porteria"
                ruta = "C:\\Users\\usuario\\Desktop\\pdf_facturas\\LEMONT1PORTERIA_fACTURA.pdf"
                ruta_pdf = os.path.join(appdata_path, ruta)
                return asunto, ruta_pdf

            case _:
                return "error no hay planta"
