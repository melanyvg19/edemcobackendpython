import pyodbc
#Prueba para conectar la bd
class connection_db():

   DB_CONFIG = {
        'DRIVER': '{ODBC Driver 17 for SQL Server}',
        'SERVER': '10.255.252.2',
        'DATABASE': 'edemco',
        'UID': 'temptech',
        'PWD': 'Edemco2024*+'
    }
    
# Inicialización del objeto antes de establecer conexión a la db
   def __init__(self):
         self.conn = None
         self.cursor = None

# Configuración de la conexión a la base de datos
   def connect_db(self):
        try:
            conn_str = (
                f"DRIVER={self.DB_CONFIG['DRIVER']};"
                f"SERVER={self.DB_CONFIG['SERVER']};"
                f"DATABASE={self.DB_CONFIG['DATABASE']};"
                f"UID={self.DB_CONFIG['UID']};"
                f"PWD={self.DB_CONFIG['PWD']}"
            )
            self.conn = pyodbc.connect(conn_str)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")

# Cerrar conexión y cursor de la base de datos
   def close_db(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

# Ejecutar y obtener consultas
   def query_values_db(self, query):
        try:
            self.connect_db()
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result if result else None
        except Exception as e:
            print(f"Hubo un error en la consulta: {e}")
            return None
        finally:
            self.close_db()