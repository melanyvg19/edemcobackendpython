# Documentación de Microservicios en Python

## Introducción

Este documento proporciona detalles sobre los microservicios desarrollados en Python, incluyendo los puertos en los que se ejecutan, las funcionalidades que ofrecen, endpoints y las dependencias requeridas.

## Microservicio: Historic Factories

### Descripción

Este microservicio se encarga de gestionar la consulta de datos históricos de generación de plantas eléctricas. Permite obtener información basada en el NIT del cliente, el mes y el año de generación.

### Puerto

- 8090

### Endpoints

- GET /api/historico_plantas
  - Parámetros de consulta:
    - NIT Cliente, Mes de generación y Año de generación.

### Dependencias y Frameworks

- Flask 2.3.2
- Flas-CORS 3.0.10
- psycopg2: 2.9.6 (Adaptador de base de datos PostgreSQL para python)

### Ejemplo de Código

```python
# conexionbd.py
import psycopg2

class Conexion:
    @staticmethod
    def conectar():
        try:
            connection = psycopg2.connect(
                host='your_host',
                user='your_user',
                password='your_password',
                database='your_database',
                port='your_port'
            )
            return connection.cursor()
        except Exception as ex:
            print(ex)
            return None

# consultas.py
from conexionbd import Conexion
import json

class Consulta:
    @staticmethod
    def consultar(nit, mes, anio):
        cur = Conexion.conectar()
        if not cur:
            return json.dumps({"status": 500, "title": "INTERNAL_SERVER_ERROR", "message": "Error de conexión"})

        datos = []

        try:
            if nit and not mes and not anio:
                cur.execute('''SELECT * FROM generacion WHERE nit_cliente = %s''', (nit,))
            elif not nit and mes and anio:
                cur.execute('''SELECT * FROM generacion WHERE anio = %s AND mes = %s''', (anio, mes))
            elif nit and mes and anio:
                cur.execute('''SELECT * FROM generacion WHERE nit_cliente = %s AND anio = %s AND mes = %s''', (nit, anio, mes))
            else:
                return json.dumps({"status": 404, "title": "NOT_FOUND", "message": "No hay datos para la consulta"})

            datos = cur.fetchall()
            if not datos:
                return json.dumps({"status": 404, "title": "NOT_FOUND", "message": "No se encontraron datos"})

            return json.dumps(datos)

        except Exception as e:
            return json.dumps({"status": 500, "title": "INTERNAL_SERVER_ERROR", "message": str(e)})

# microservice.py
from consultas import Consulta

class Microservice:
    @staticmethod
    def ejecucion(nit, mes, anio):
        return Consulta.consultar(nit, mes, anio)

# main.py
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/historico_plantas', methods=['GET'])
def historico_plantas():
    nit = request.args.get('nit')
    mes = request.args.get('mes')
    anio = request.args.get('anio')
    return Microservice.ejecucion(nit, mes, anio)

if __name__ == "__main__":
    app.run(debug=True, port=8090)

```

## Microservicio: Template Facturas

### Descripción

Este microservicio se encarga de generar las facturas en PDF con base en la información que viene desde growatt.

Con base en unas macros que están en excel, genera las plantillas en PDF.

### A tener en cuenta

- El correo y la contraseña que se registra en el aplicativo, deben ser exactamente los mismos que las credenciales de outlook.

- Hay que cambiar las rutas de: la imagen que se enviará en el correo, las rutas de las macros de excel y las rutas de los archivos que se van a generar en PDF.

### Puerto

- 8091

### Endpoints

- Método para generar las plantillas: **/api/generar_template**

Recibe los siguientes parámetros por el body:

{
  'cod_planta',
  'fecha_inicio',
  'fecha_fin',
  'dias_consumo',
  'consumo_actual',
  'consumo_acumulado',
  'concepto_facturado',
  'cantidad',
  'costo_unidad',
  'valor_total',
  'fecha_pago',
  'factura_mes',
  'numero_factura',
  'contrato_no',
  'ahorro_actual',
  'ahorro_acumulado',
  'periodo_actual', #ahorro_codos_actual
  'periodo_acumulado', #ahorro_codos_acumulado
  'cufe',
  'fecha_cufe'
}

### Dependencias y Frameworks

- flask==2.3.2
- flask-cors==3.0.10
- xlwings==0.29.0
- smtplib3==1.0
- email==6.0.0
- psycopg2==2.9.6

### Ejemplo de Código

```js
conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor(cursor_factory=RealDictCursor)
cursor.execute("""
    SELECT e.email 
    FROM email e
    JOIN planta p ON e.id_planta = p.id_planta
    WHERE e.id_planta = %s
""", (cod_planta,))
result = cursor.fetchall()

email_list = [row['email'] for row in result]
```

## Microservicio: Get Invoice

### Descripción

<!-- Descripción del microservicio -->

Get invoice este microservicio proporciona una API REST que permite a los usuarios obtener datos de facturación desde una base de datos PostgreSQL. Está construido utilizando Flask para la parte web y SQLAlchemy para interactuar con la base de datos. Los datos de facturación incluyen información detallada sobre plantas, facturas, clientes y generación de energía.

### Puerto

- 8092

### Endpoints

- http://localhost:8092/api/facturas

### Dependencias y Frameworks

- flask==3.0.3
- flask-cors==3.0.10
- sqlalchemy==2.0.31

### Ejemplo de Código

```python
@cross_origin
@app.route("/api/facturas", methods=["GET"])
def get_facturas():
    session = SessionLocal()
    results = session.query(
        Planta.id_planta.label('cod_planta'),
        Planta.nombre_planta.label('nombre_planta'),
        Factura.fecha_inicial.label('fecha_inicio'),
        Factura.fecha_final.label('fecha_fin'),
        Factura.dias_facturados.label('dias_consumo'),
        Factura.numero_factura.label('numero_factura'),
        Factura.concepto_facturado.label('concepto_facturado'),
        Factura.cufe.label('cufe'),
        Factura.fecha_dian.label('fecha_cufe'),
        Factura.fecha_pago.label('fecha_pago'),
        Cliente.contrato.label('contrato_no'),
        Generacion.generacion_actual.label('cantidad'),
        Generacion.ahorro_acumulado.label('ahorro_acumulado'),
        Generacion.mes.label('factura_mes'),
        Generacion.generacion_actual.label('consumo_actual'),
        Generacion.generacion_acumulado.label('consumo_acumulado'),
        Generacion.ahorro_actual.label('ahorro_actual'),
        Generacion.valor_unidad.label('costo_unidad'),
        Generacion.valor_total.label('valor_total'),
        Generacion.ahorro_codos_actual.label('periodo_actual'),
        Generacion.ahorro_codos_acumulado.label('periodo_acumulado')
    ).join(
        Factura, Factura.id_planta == Planta.id_planta
    ).join(
        Cliente, Cliente.id_cliente == Planta.id_cliente
    ).join(
        Generacion, Generacion.id_planta == Planta.id_planta
    ).all()

    session.close()
```

## Microservicio: Upload File

### Descripción

<!-- Descripción del microservicio -->

Upload File Este microservicio proporciona una API REST que permite a los usuarios cargar un archivo Excel, procesar sus datos y devolver un resultado en formato JSON. Está construido utilizando Flask para la parte web y pandas para el procesamiento de datos. A continuación, se detallan los componentes y funcionalidades principales del microservicio.

### Puerto

- 8093

### Endpoints

- http://127.0.0.1:5000/api/upload_excel

### Dependencias y Frameworks

- Flask==3.0.3
- Flask_Cors==4.0.1
- pandas==2.2.2
- python-dateutil==2.9.0

### Ejemplo de Código

```python
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

```

## Microservicio: Growatt Generation

### Descripción

Este microservicio está diseñado para automatizar la interacción con la página web de Growatt utilizando Selenium, descargar un archivo Excel con datos de generación de energía, procesar los datos y devolverlos en formato JSON. El servicio se divide en dos partes principales: Microservice_1 para la automatización de la descarga y Microservice_2 para el procesamiento de los datos.

### Puerto

- 8094

### Endpoints

- /api/growatt

### Dependencias y Frameworks

- Flask 2.3.2
- Flas-CORS 3.0.10
- Selenium 4.19.0

### Ejemplo de Código

```python
# main.py
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from microservice1 import Microservice1
from microservice2 import Microservice2

app = Flask(__name__)
CORS(app)

microservice1 = Microservice1()
microservice2 = Microservice2()

@cross_origin
@app.route('/api/growatt')
def home():
    microservice1.execute()
    json_data = microservice2.execute()
    return jsonify(json_data)

if __name__ == '__main__':
    app.run(debug=True, port=8094)

```
