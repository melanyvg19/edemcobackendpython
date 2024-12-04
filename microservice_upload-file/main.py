from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from microservice import Microservice


app = Flask(__name__)
CORS(app)


@cross_origin
@app.route('/api/upload_excel', methods=['POST'])
def upload_excel():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        micro_instancia = Microservice()
        file_json = micro_instancia.execute(file)

        return file_json 

if __name__ == '__main__':
    app.run(debug=True, port=8093)
