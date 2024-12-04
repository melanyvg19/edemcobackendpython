# Importamos flask, request, jsonify
from flask import Flask, request
from flask_cors import CORS, cross_origin
from microservice import microservice

app = Flask(__name__)


CORS(app)


# Se declara el End point
@cross_origin
@app.route("/api/historico_plantas", methods=["GET"])
def microservice_init():
    # Los argumentos se convierten en variables
    idPlanta = request.args.get("idPlanta")
    mes = request.args.get("mes")
    anio = request.args.get("anio")

    # Si las 3 variables no tienen valor retornameros el mensaje
    json_file = microservice.ejecucion(idPlanta, mes, anio)
    return json_file


if __name__ == "__main__":
    app.run(debug=True, port=8090)
