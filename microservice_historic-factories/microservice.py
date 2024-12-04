from consultas import Consulta

class microservice(Consulta):
    
    def ejecucion(idPlanta, mes, anio):
        json_file = Consulta.consultar(idPlanta, mes, anio)
        return json_file