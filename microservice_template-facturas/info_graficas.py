from graficas_template import GraficaExcel

 #procesamiento a los archivos
class DTO_Graficas():

    def ejecucion(self, cod_planta, ruta_archivo):
        grafica_excel = GraficaExcel() 
        grafica_excel.process_excel(cod_planta, ruta_archivo)
