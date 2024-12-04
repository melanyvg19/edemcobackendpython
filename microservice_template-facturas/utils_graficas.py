
class utils_graficas():
    # nombre hoja excel
    def select_planta_excel(self, cod_planta):
        match cod_planta:
            case "506":
                #Ceipa Barranquilla
                nombre = 'CEIPABARRANQUIL_GRAPHICS'
                return nombre

            case "508":
                #Liceo Frances
                nombre = 'LICEOFRANCESSFV_GRAPHICS'
                return nombre
                
            case "514":
                #Incubant
                nombre = 'INCUBANSSFV_GRAPHICS'
                return nombre
                
            case "505":
                #Punto clave
                nombre = 'PUNTOCLAVESSFV_GRAPHICS'
                return nombre

            case "512":
                #Lemont Salon Social
                nombre = 'LEMONTSALONSOC_GRAPHICS'
                return nombre

            case "513":
                #Pollocoa
                nombre = 'POLLOCOASSFV_GRAPHICS'
                return nombre
                
            case "507":
                #Ceipa Sabaneta
                nombre = 'CEIPASABANETASS_GRAPHICS'
                return nombre
                
            case "511":
                #lemont Porteria
                nombre = 'LEMONTPORT_GRAPHICS'
                return nombre
                
            case _:
                return 'error selección planta excel'