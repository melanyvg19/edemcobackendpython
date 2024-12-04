from abc import ABC, abstractmethod
import xlwings as xw

# La clase Template es una clase abstracta que define una interfaz común para todas las clases que la hereden.
class Template(ABC):

    # El método execute es el método principal que se encarga de ejecutar los pasos necesarios para procesar un archivo de Excel.
    def execute(self,ruta_archivo, planta, fechaIni,fechaFin,diasConsumo,consumoActual,consumoAcumulado,conceptoFacturado,Cantidad,costoUnidad,valorTotal,fechaPago,facturaMes,facturaNo,contratoNo,ahorroActual,ahorroAcumulado,periodoActual,periodoAcumulado,CUFE,fechaCUFE):
        
        #wb = xw.Book(r'c:\Users\Temp Tech\Desktop\macros_factura\FACTURA_LEMONT_ACTUALIZADA.xlsm')
        # Abre el archivo de Excel ubicado en la ruta especificada.
        wb = xw.Book(ruta_archivo)

        # Selecciona la hoja de cálculo correspondiente a la planta especificada.
        sheet = self.selectsheet(wb, planta)

        # Establece los valores en la hoja de cálculo con los datos proporcionados.
        self.setvalue(sheet,fechaIni,fechaFin,diasConsumo,consumoActual,consumoAcumulado,conceptoFacturado,Cantidad,costoUnidad,valorTotal,fechaPago,facturaMes,facturaNo,contratoNo,ahorroActual,ahorroAcumulado,periodoActual,periodoAcumulado,CUFE,fechaCUFE)

        # Guarda y cierra el archivo de Excel.
        self.save(wb)
        
        
    # Método abstracto para seleccionar una hoja de cálculo. Debe ser implementado por las clases que hereden de Template.
    @abstractmethod
    def selectsheet(self,wb):
        pass

    # Método abstracto para establecer los valores en una hoja de cálculo. Debe ser implementado por las clases que hereden de Template.
    @abstractmethod
    def setvalue(self,fechaIni,fechaFin,diasConsumo,consumoActual,consumoAcumulado,conceptoFacturado,Cantidad,costoUnidad,valorTotal,fechaPago,facturaMes,facturaNo,contratoNo,ahorroActual,ahorroAcumulado,periodoActual,periodoAcumulado,CUFE,fechaCUFE):
        pass

    # Método abstracto para guardar y cerrar un archivo de Excel. Debe ser implementado por las clases que hereden de Template.
    @abstractmethod
    def save(self):
        pass