import pyodbc

class Conexion:
    @staticmethod
    def conectar():
        try:
            # Credenciales de conexión y rutas para SQL Server
            connection = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=10.255.252.2;'
                'DATABASE=edemco;'
                'UID=temptech;'
                'PWD=Edemco2024*+'
            )
        except Exception as ex:
            print(ex)

        # Creamos el cursor para manipular consultas en nuestra base de datos
        cur = connection.cursor()
        return cur
