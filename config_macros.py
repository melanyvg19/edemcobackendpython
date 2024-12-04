import os
import win32com.client
import time


class ConfigMacros:

    @staticmethod
    def ejecutar(ruta, nombre_archivo, ruta_pdf):
        # Obtener la ruta APPDATA
        if os.path.exists(ruta):

            # Obtener el nombre del archivo sin la ruta
            file_name = os.path.basename(nombre_archivo)

            # Verificar si el archivo tiene la extensión correcta
            if not file_name.endswith(".xlsm"):
                raise ValueError("El archivo debe tener la extensión .xlsm")

            # Quitar la extensión .xlsm
            file_name_no_ext = file_name[:-5]

            # Dividir el nombre del archivo para reordenarlo
            parts = file_name_no_ext.split("_")
            if len(parts) < 2:
                raise ValueError("El nombre del archivo no tiene el formato esperado")

            # Crear el nuevo nombre del archivo
            new_file_name = (
                f"{parts[1]}_{parts[0].lower().replace('factura', 'factura')}.pdf"
            )

            print(parts[1])
            # Crear la ruta completa al nuevo archivo
            new_file_path = os.path.join(ruta_pdf, new_file_name)

            print("Nueva ruta del archivo:", new_file_path)

            macro_string = f"""Sub SaveAsPDF()
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Sheets("{parts[1]}") ' Cambia "Sheet1" por el nombre de tu hoja
    Set Rng = ws.Range("A1:J49")

    Rng.ExportAsFixedFormat Type:=xlTypePDF, Filename:="{new_file_path}"
End Sub
"""
            excel_app = win32com.client.Dispatch("Excel.Application")
            excel_app.Visible = False  # No muestra la interfaz de Excel
            libro = excel_app.Workbooks.Open(ruta)

            try:
                # Accede al módulo de VBA donde se encuentra la macro
                modulo_vba = libro.VBProject.VBComponents("Módulo1")

                # Reemplaza "Modulo1" por el nombre de tu módulo
                lineas = modulo_vba.CodeModule.CountOfLines

                # Sobreescribe el contenido de la macro con el nuevo contenido
                modulo_vba.CodeModule.DeleteLines(1, lineas)
                modulo_vba.CodeModule.AddFromString(macro_string)

                # Guarda los cambios y cierra el archivo
                libro.Save()
                print("La macro ha sido modificada y guardada.")
                time.sleep(10)
            except Exception as e:
                print(f"Error al modificar la macro: {e}")
            finally:
                libro.Close()
                excel_app.Quit()
