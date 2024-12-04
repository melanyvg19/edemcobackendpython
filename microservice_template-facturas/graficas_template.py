import xlwings as xw
from utils_graficas import utils_graficas
import os
from connection_db import connection_db
import time

class GraficaExcel():
   # Crear instancia de connection_db
    def __init__(self):
        self.db = connection_db()

    # Actualizar el archivo excel
    def update_excel(self, ruta_archivo, hoja, data):
        try:
            wb = xw.Book(ruta_archivo)
            sheet = wb.sheets[hoja]
            if hoja == "PUNTOCLAVESSFV_GRAPHICS":
                for celda, row in enumerate(data):
                    sheet.range(f"B{6 + celda}").value = row[0]  # fecha
                    sheet.range(f"C{6 + celda}").value = row[1]  # Generacion
                    sheet.range(f"D{6 + celda}").value = row[2]  # Exportacion
                    sheet.range(f"G{6 + celda}").value = row[3]  # VALOR kWh
                    sheet.range(f"I{6 + celda}").value = row[4]  # Tarifa OR
                    sheet.range(f"M{6 + celda}").value = row[5]  # Ahorro actual

            else:
                for celda, row in enumerate(data):
                    sheet.range(f"B{6 + celda}").value = row[0]  # fecha
                    sheet.range(f"C{6 + celda}").value = row[1]  # Generacion
                    sheet.range(f"E{6 + celda}").value = row[3]  # VALOR kWh
                    sheet.range(f"G{6 + celda}").value = row[4]  # Tarifa OR
                    sheet.range(f"J{6 + celda}").value = row[5]  # Ahorro actual
            wb.save()
            wb.close()
            print("Se debió haber cerrado")
            os.system("taskkill /F /IM excel.exe")
            time.sleep(10)
        except Exception as e:
            print(f"Hubo un error al actualizar el archivo Excel: {e}")

    # Realizar actualizaciones en archivos excel
    def process_excel(self, cod_planta, ruta_archivo):
        query = f'''
            SELECT 
                CASE 
                    WHEN sub.mes = 1 THEN 'Ene'
                    WHEN sub.mes = 2 THEN 'Feb'
                    WHEN sub.mes = 3 THEN 'Mar'
                    WHEN sub.mes = 4 THEN 'Abr'
                    WHEN sub.mes = 5 THEN 'May'
                    WHEN sub.mes = 6 THEN 'Jun'
                    WHEN sub.mes = 7 THEN 'Jul'
                    WHEN sub.mes = 8 THEN 'Ago'
                    WHEN sub.mes = 9 THEN 'Sep'
                    WHEN sub.mes = 10 THEN 'Oct'
                    WHEN sub.mes = 11 THEN 'Nov'
                    WHEN sub.mes = 12 THEN 'Dic'
                END + '-' + RIGHT(CAST(sub.anio AS VARCHAR(4)), 2) AS fecha,
                sub.generacion_actual AS Generacion,
                e.valor_exportacion AS [Exportación],
                sub.valor_unidad AS [VALOR kWh],
                sub.tarifa_operador AS [Tarifa OR],
                sub.ahorro_actual AS [Ahorro actual]
            FROM (
                SELECT TOP 6
                    g.mes,
                    g.anio,
                    g.generacion_actual,
                    g.valor_unidad,
                    o.tarifa_operador,
                    g.ahorro_actual
                FROM 
                    generacion g
                INNER JOIN tarifa_operadores o ON g.id_tarifa_operador = o.id_tarifa_operador
                WHERE g.id_planta = '{cod_planta}'
                ORDER BY 
                    g.anio DESC, g.mes DESC
            ) sub
            INNER JOIN facturacion_especial e ON sub.mes = e.mes AND sub.anio = e.anio
            ORDER BY sub.anio ASC, sub.mes ASC;
        '''
        
        select = utils_graficas()
        data = self.db.query_values_db(query)
        if data:
            print("consulta:", data)
            hoja = select.select_planta_excel(cod_planta)
            self.update_excel(ruta_archivo, hoja, data)

