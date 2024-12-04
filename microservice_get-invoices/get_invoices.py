from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from sqlalchemy import create_engine, Column, String, Integer, Date, Double, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

DATABASE_URL = "mssql+pyodbc://temptech:Edemco2024*+@10.255.252.2/edemco?driver=ODBC+Driver+17+for+SQL+Server"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Planta(Base):
    __tablename__ = 'planta'
    id_planta = Column(String, primary_key=True)
    nombre_planta = Column(String, nullable=False)
    facturas = relationship('Factura', back_populates='planta')
    generacion = relationship('Generacion', back_populates='planta')
    id_cliente = Column(Integer, ForeignKey('cliente.id_cliente'))

class Factura(Base):
    __tablename__ = 'factura'
    id_factura = Column(Integer, primary_key=True)
    fecha_inicial = Column(Date)
    fecha_final = Column(Date)
    dias_facturados = Column(Integer)
    cufe = Column(String)
    fecha_dian = Column(Date)
    fecha_pago = Column(Date)
    numero_factura = Column(String)
    concepto_facturado = Column(String)  # Cambiado de Text a String
    id_planta = Column(String, ForeignKey('planta.id_planta'))
    planta = relationship('Planta', back_populates='facturas')

class Cliente(Base):
    __tablename__ = 'cliente'
    id_cliente = Column(Integer, primary_key=True)
    contrato = Column(String)

class Generacion(Base):
    __tablename__ = 'generacion'
    id_generacion = Column(Integer, primary_key=True)
    generacion_actual = Column(Double)
    generacion_acumulado = Column(Double)
    valor_unidad = Column(Double)
    valor_total = Column(Double)
    ahorro_acumulado = Column(Double)
    mes = Column(Integer)
    ahorro_actual = Column(Double)
    ahorro_codos_actual = Column(Double)
    ahorro_codos_acumulado = Column(Double)
    id_planta = Column(String, ForeignKey('planta.id_planta'))
    planta = relationship('Planta', back_populates='generacion')

Base.metadata.create_all(bind=engine)

@cross_origin
@app.route("/api/facturas", methods=["GET"])
def get_facturas():
    session = SessionLocal()
    try:
        hoy = datetime.now()
        primer_dia_mes_actual = hoy.replace(day=1)
        mes_anterior = primer_dia_mes_actual - timedelta(days=1)
        mes_anterior_numero = mes_anterior.month
        año_mes_anterior = mes_anterior.year

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
        ).filter(
            func.month(Factura.fecha_inicial) == mes_anterior_numero,
            func.year(Factura.fecha_inicial) == año_mes_anterior,
            func.month(Factura.fecha_final) == mes_anterior_numero,
            func.year(Factura.fecha_final) == año_mes_anterior,
            Generacion.mes == mes_anterior_numero,
            Factura.cufe.isnot(None)
        ).group_by(
            Planta.id_planta,
            Factura.id_factura,
            Generacion.id_generacion,
            Planta.nombre_planta,
            Factura.fecha_inicial,
            Factura.fecha_final,
            Factura.dias_facturados,
            Factura.numero_factura,
            Factura.concepto_facturado,
            Factura.cufe,
            Factura.fecha_dian,
            Factura.fecha_pago,
            Cliente.contrato,
            Generacion.generacion_actual,
            Generacion.ahorro_acumulado,
            Generacion.mes,
            Generacion.generacion_acumulado,
            Generacion.ahorro_actual,
            Generacion.valor_unidad,
            Generacion.valor_total,
            Generacion.ahorro_codos_actual,
            Generacion.ahorro_codos_acumulado
        )

        def format_date(date_obj):
            if date_obj:
                return date_obj.strftime('%Y/%m/%d')
            return None

        def format_currency(value):
            return "${:,.2f}".format(value).replace(",", "X").replace(".", ",").replace("X", ".")

        sessionend = []
        for row in results:
            row_dict = row._asdict()
            row_dict['fecha_inicio'] = format_date(row_dict['fecha_inicio'])
            row_dict['fecha_fin'] = format_date(row_dict['fecha_fin'])
            row_dict['fecha_cufe'] = format_date(row_dict['fecha_cufe'])
            row_dict['fecha_pago'] = format_date(row_dict['fecha_pago'])
            row_dict['valor_total'] = format_currency(row_dict['valor_total'])
            sessionend.append(row_dict)

        return jsonify(sessionend)
    
    finally:
        session.close()


if __name__ == "__main__":
    app.run(debug=True, port=8092)
