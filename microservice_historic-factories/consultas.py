from conexionbd import Conexion
import json

class Consulta(Conexion):

    @staticmethod
    def consultar(idPlanta, mes, anio):
        # Nos traemos el cursor desde Conexion
        cur = Conexion.conectar()
        # Declaramos una lista
        datos = []

        # Validación de entradas y conversión a None si es necesario
        idPlanta = str(idPlanta) if idPlanta and idPlanta != "0" else None
        mes = int(mes) if mes and mes != "0" else None
        anio = int(anio) if anio and anio != "0" else None

        try:
            if idPlanta and not mes and not anio:
                # Consultar basada solo en el idPlanta
                cur.execute('''SELECT g.*, p.nombre_planta
                               FROM generacion AS g
                               INNER JOIN planta AS p ON g.id_planta = p.id_planta
                               WHERE p.id_planta = ?''', (idPlanta,))
            elif not idPlanta and mes and anio:
                # Consultar basada solo en mes y anio
                cur.execute('''SELECT g.*, p.nombre_planta
                               FROM generacion AS g
                               INNER JOIN planta AS p ON g.id_planta = p.id_planta
                               WHERE g.anio = ? AND g.mes = ?''', (anio, mes))
            elif idPlanta and mes and anio:
                # Consultar basada en todos los parámetros
                cur.execute('''SELECT g.*, p.nombre_planta
                               FROM generacion AS g
                               INNER JOIN planta AS p ON g.id_planta = p.id_planta
                               WHERE p.id_planta = ? AND g.anio = ? AND g.mes = ?''', (idPlanta, anio, mes))
            else:
                # Si no hay suficientes datos para la consulta
                error_json = {
                    "status": 404,
                    "title": "NOT_FOUND",
                    "message": "No hay datos para la factura"
                }
                return json.dumps(error_json)
                
            for row in cur.fetchall():
                datos.append({
                    "id_generacion": row[0],
                    "generacion_actual": row[1],
                    "generacion_acumulado": row[2],
                    "valor_unidad": row[3],
                    "valor_total": row[4],
                    "diferencia_tarifa": row[5],
                    "ahorro_actual": row[6],
                    "ahorro_acumulado": row[7],
                    "ahorro_codos_actual": row[8],
                    "ahorro_codos_acumulado": row[9],
                    "anio": row[10],
                    "mes": row[11],
                    "nit_cliente": row[12],
                    "id_planta": row[14]
                })
                
        except Exception as e:
            error_json = {
                "status": 500,
                "title": "INTERNAL_SERVER_ERROR",
                "message": str(e)
            }
            return json.dumps(error_json)

        if not datos:
            error_json = {
                "status": 404,
                "title": "NOT_FOUND",
                "message": "Los datos no han sido encontrados"
            }
            return json.dumps(error_json)
        
        # Retornamos la lista
        return json.dumps(datos)
