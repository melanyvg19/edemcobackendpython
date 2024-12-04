from facturacion import facturacion_normal
from facturacion import facturacion_especial
from info_graficas import DTO_Graficas
import os


class microservice_factura:
    def seleccion_template(
        self,
        cod_planta,
        fechaIni,
        fechaFin,
        diasConsumo,
        consumoActual,
        consumoAcumulado,
        conceptoFacturado,
        Cantidad,
        costoUnidad,
        valorTotal,
        fechaPago,
        facturaMes,
        facturaNo,
        contratoNo,
        ahorroActual,
        ahorroAcumulado,
        periodoActual,
        periodoAcumulado,
        CUFE,
        fechaCUFE,
    ):
        # Agregamos un print para verificar los parámetros recibidos
        print("Parametros recibidos:")
        print(f"cod_planta: {cod_planta}, fechaIni: {fechaIni}, fechaFin: {fechaFin}, diasConsumo: {diasConsumo}")
        print(f"consumoActual: {consumoActual}, consumoAcumulado: {consumoAcumulado}, conceptoFacturado: {conceptoFacturado}")
        print(f"Cantidad: {Cantidad}, costoUnidad: {costoUnidad}, valorTotal: {valorTotal}")
        print(f"fechaPago: {fechaPago}, facturaMes: {facturaMes}, facturaNo: {facturaNo}")
        print(f"contratoNo: {contratoNo}, ahorroActual: {ahorroActual}, ahorroAcumulado: {ahorroAcumulado}")
        print(f"CUFE: {CUFE}, fechaCUFE: {fechaCUFE}")

        instacia_graficas = DTO_Graficas()
        appdata_path = os.getenv("APPDATA")

        # Agregar print para verificar la ruta del archivo
        print("Ruta base APPDATA:", appdata_path)

        match cod_planta:
            case "506":
                planta = "CEIPABARRANQUIL"
                ruta = "C:\\Users\\usuario\\Desktop\\macro_factura\\FACTURA_CEIPABARRANQUIL.xlsm"
                ruta_archivo = os.path.join(appdata_path, ruta)
                instacia_graficas.ejecucion(cod_planta, ruta_archivo)
                print('case1', ruta_archivo)

            case "508":
                planta = "LICEOFRANCESSFV"
                ruta = "C:\\Users\\usuario\\Desktop\\macro_factura\\FACTURA_LICEOFRANCESSFV.xlsm"
                ruta_archivo = os.path.join(appdata_path, ruta)
                instacia_graficas.ejecucion(cod_planta, ruta_archivo)
                print('case2', ruta_archivo)

            case "514":
                planta = "INCUBANSSFV"
                ruta = "C:\\Users\\usuario\\Desktop\\macro_factura\\FACTURA_INCUBANSSFV.xlsm"
                ruta_archivo = os.path.join(appdata_path, ruta)
                instacia_graficas.ejecucion(cod_planta, ruta_archivo)
                print('case3', ruta_archivo)

            case "505":
                planta = "PUNTOCLAVESSFV"
                ruta = "C:\\Users\\usuario\\Desktop\\macro_factura\\FACTURA_PUNTOCLAVESSFV.xlsm"
                ruta_archivo = os.path.join(appdata_path, ruta)
                instacia_graficas.ejecucion(cod_planta, ruta_archivo)
                print('case4', ruta_archivo)

            case "512":
                planta = "LEMONT1SALONSOC"
                ruta = "C:\\Users\\usuario\\Desktop\\macro_factura\\FACTURA_LEMONT1SALONSOC.xlsm"
                ruta_archivo = os.path.join(appdata_path, ruta)
                instacia_graficas.ejecucion(cod_planta, ruta_archivo)
                print('case5', ruta_archivo)

            case "513":
                planta = "POLLOCOASSFV"
                ruta = "C:\\Users\\usuario\\Desktop\\macro_factura\\FACTURA_POLLOCOASSFV.xlsm"
                ruta_archivo = os.path.join(appdata_path, ruta)
                instacia_graficas.ejecucion(cod_planta, ruta_archivo)
                print('case6', ruta_archivo)

            case "507":
                planta = "CEIPASABANETASS"
                ruta = "C:\\Users\\usuario\\Desktop\\macro_factura\\FACTURA_CEIPASABANETASS.xlsm"
                ruta_archivo = os.path.join(appdata_path, ruta)
                instacia_graficas.ejecucion(cod_planta, ruta_archivo)
                print('case7', ruta_archivo)

            case "511":
                planta = "LEMONT1PORTERIA"
                ruta = "C:\\Users\\usuario\\Desktop\\macro_factura\\FACTURA_LEMONT1PORTERIA.xlsm"
                ruta_archivo = os.path.join(appdata_path, ruta)
                instacia_graficas.ejecucion(cod_planta, ruta_archivo)
                print('case8', ruta_archivo)

            case _:
                print('caseFinal')
                return "error no hay planta"

        # Verificar si factura_normal o factura_especial es llamada
        if cod_planta != "505":
            print("Usando facturacion_normal")
            factura = facturacion_normal()
        else:
            print("Usando facturacion_especial")
            factura = facturacion_especial()

        # Imprimir antes de ejecutar el método 'execute'
        print("Ejecutando factura con los siguientes parámetros:")
        print(f"ruta_archivo: {ruta_archivo}, planta: {planta}")

        factura.execute(
            ruta_archivo,
            planta,
            fechaIni,
            fechaFin,
            diasConsumo,
            consumoActual,
            consumoAcumulado,
            conceptoFacturado,
            Cantidad,
            costoUnidad,
            valorTotal,
            fechaPago,
            facturaMes,
            facturaNo,
            contratoNo,
            ahorroActual,
            ahorroAcumulado,
            periodoActual,
            periodoAcumulado,
            CUFE,
            fechaCUFE,
        )
        print("Factura generada correctamente")
