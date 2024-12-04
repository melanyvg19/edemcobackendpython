# Importamos las librerías necesarias
from flask import Flask, jsonify # Flask para crear la aplicación web y jsonify para convertir datos a formato JSON
from flask_cors import CORS, cross_origin
from microservice_1 import Microservice_1  # Importamos la clase Microservice_1 de microservice_1.py
from microservice_2 import Microservice_2  # Importamos la clase Microservice_2 de microservice_2.py

# Creamos una instancia de la aplicación Flask
app = Flask(__name__)
CORS(app)
# Creamos instancias de Microservice_1 y Microservice_2
microservice_1 = Microservice_1()
microservice_2 = Microservice_2()

# Definimos la ruta '/Growatt' y su controlador
@cross_origin
@app.route('/api/growatt')
def home():
    # Ejecutamos el método execute de microservice_1
    microservice_1.execute()
    json_data = microservice_2.execute()
    # Devolvemos un mensaje al usuario
    return jsonify(json_data)

# Comprobamos si este archivo es el punto de entrada principal para ejecutar la aplicación
if __name__ == '__main__':
    # Ejecutamos la aplicación Flask en modo debug (los cambios en el código se reflejarán automáticamente sin necesidad de reiniciar el servidor)
    app.run(debug=True, port=8094)
