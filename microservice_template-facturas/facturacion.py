import xlwings as xw
import os
from template import Template
from connection_db import connection_db

class facturacion_normal(Template):
    
    # Método para seleccionar una hoja de un libro de trabajo
    def selectsheet(self, wb, planta):
        # Selecciona la hoja llamada 'planta' del libro de trabajo 'wb'
        sheet = wb.sheets[planta]
        # Devuelve la hoja seleccionada
        return sheet
    
    # Método para establecer valores en una hoja
    def setvalue(self,sheet,fechaIni,fechaFin,diasConsumo,consumoActual,consumoAcumulado,conceptoFacturado,Cantidad,costoUnidad,valorTotal,fechaPago,facturaMes,facturaNo,contratoNo,ahorroActual,ahorroAcumulado,periodoActual,periodoAcumulado,CUFE,fechaCUFE):
        # Establece los valores en las celdas especificadas de la hoja
        sheet.range('O52').value = fechaIni
        sheet.range('O53').value = fechaFin
        sheet.range('O54').value = diasConsumo
        sheet.range('O55').value = consumoActual
        sheet.range('O56').value = consumoAcumulado
        sheet.range('O57').value = conceptoFacturado
        sheet.range('O58').value = Cantidad
        sheet.range('O59').value = costoUnidad
        sheet.range('O60').value = valorTotal
        sheet.range('O61').value = fechaPago
        sheet.range('O62').value = facturaMes
        sheet.range('O63').value = facturaNo
        sheet.range('O64').value = contratoNo
        sheet.range('O65').value = ahorroActual
        sheet.range('O66').value = ahorroAcumulado
        sheet.range('O67').value = periodoActual
        sheet.range('O68').value = periodoAcumulado
        sheet.range('O69').value = CUFE
        sheet.range('O70').value = fechaCUFE
    
    # Método para guardar y cerrar un libro de trabajo
    def save(self, wb):
        # Guarda el libro de trabajo 'wb'
        wb.save()
        # Ejecuta la macro de excel
        wb.macro("SaveAsPDF")()
        # Cierra el libro de trabajo 'wb'
        wb.close()
        # Matar todos los procesos de Excel
        os.system("taskkill /F /IM excel.exe")  

class facturacion_especial():

    # Crear instancia de connection_db
   def __init__(self):
        self.db = connection_db()

   def execute(self, ruta_archivo, planta, fechaIni, fechaFin, diasConsumo, consumoActual, consumoAcumulado, conceptoFacturado, Cantidad, costoUnidad, valorTotal, fechaPago, facturaMes, facturaNo, contratoNo, ahorroActual, ahorroAcumulado, periodoActual, periodoAcumulado, CUFE, fechaCUFE):
        try:
            wb = xw.Book(ruta_archivo)
            sheet = wb.sheets[planta]
    
            query = f''' SELECT TOP 1 e.valor_exportacion AS "Exportación tarifa", e.cantidad_kwh AS "Exportación kWh" from facturacion_especial e 
            INNER JOIN generacion g ON e.id_planta = g.id_planta
            WHERE e.mes = g.mes AND e.anio = g.anio
            ORDER BY e.anio DESC, e.mes DESC  '''

            consulta = self.db.query_values_db(query)
            datos = consulta[0]
            ExporTarifa = datos[0]
            ExporKwh = datos[1]
            sheet.range("O30").value = ExporTarifa
            sheet.range("O31").value = ExporKwh 
            sheet.range("O52").value = fechaIni
            sheet.range("O53").value = fechaFin
            sheet.range("O54").value = diasConsumo
            sheet.range("O55").value = consumoActual
            sheet.range("O56").value = consumoAcumulado
            sheet.range("O57").value = conceptoFacturado
            sheet.range("O58").value = Cantidad
            sheet.range("O59").value = costoUnidad
            sheet.range("O60").value = valorTotal  #valor total incluye la tarifa de la exportación
            sheet.range("O61").value = fechaPago
            sheet.range("O62").value = facturaMes
            sheet.range("O63").value = facturaNo
            sheet.range("O64").value = contratoNo
            sheet.range("O65").value = ahorroActual
            sheet.range("O66").value = ahorroAcumulado
            sheet.range("O67").value = periodoActual
            sheet.range("O68").value = periodoAcumulado
            sheet.range("O69").value = CUFE
            sheet.range("O70").value = fechaCUFE

            # Guarda el libro de trabajo 'wb'
            wb.save()
            # Ejecuta la macro de excel
            wb.macro("SaveAsPDF")()
            # Cierra el libro de trabajo 'wb'
            wb.close()
            # Matar todos los procesos de Excel
            os.system("taskkill /F /IM excel.exe")
        except Exception as e:
            print(f"Error: {e}")

