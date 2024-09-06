from flaskr import create_app
from datetime import datetime
from .modelos import db, Factura, FacturaSchema
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import requests
from celery import Celery
import json


app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)

celery_app = Celery('tasks', broker='redis://abcall:6379/0')

@celery_app.task(name='factura_log')
def registrar_log(id_factura, fecha_factura):
    print(f"Log registrado para la creación de la factura {id_factura} en {fecha_factura}")

factura_schema = FacturaSchema()
factura_single_schema = FacturaSchema()

class VistaHealth(Resource):
    def get(self):
        return 'Realizar factura está ok', 200

class VistaRealizarFactura(Resource):
    def post(self, id):
        response = requests.get(f'http://abcall:5000/usuario/{id}')
        
        if response.status_code == 404:
            return response.json(), 404
        else:
            usuario = response.json()
            factura = self.realizar_factura(usuario)
            db.session.add(factura)
            db.session.commit()
            factura_json = factura_schema.dump(factura)
            args = (factura_json['id'], factura_json['fecha'])
            registrar_log.delay(factura_json['id'], factura_json['fecha'])
            return jsonify(factura_json)

    def realizar_factura(self, usuario):
        pqr = usuario.get('PQR', 0)
        canal_comunicacion = usuario.get('canal_comunicacion')

        multiplicadores = {
            'Chat': 10,
            'Correo': 20,
            'Llamada': 30
        }

        monto = pqr * multiplicadores.get(canal_comunicacion, 1)

        factura = Factura(
            usuario_id=usuario['id'],
            nombre=usuario['nombre'],
            monto=monto,
            detalle=f'Factura generada para {canal_comunicacion}',
            estado='Generada',
            fecha=datetime.now()
        )
        
        return factura

api.add_resource(VistaRealizarFactura, '/realizar_factura/<int:id>')
api.add_resource(VistaHealth, '/health')

class VistaConsultarFactura(Resource):
    def get(self, id):
        factura = Factura.query.get(id)
        if not factura:
            return {'message': 'Factura no encontrada'}, 404
        factura_json = {
            'id': factura.id,
            'usuario_id': factura.usuario_id,
            'nombre': factura.nombre,
            'monto': factura.monto,
            'detalle': factura.detalle,
            'estado': factura.estado,
            'fecha': factura.fecha.strftime('%Y-%m-%d %H:%M:%S')
        }
        return jsonify(factura_json)

api.add_resource(VistaConsultarFactura, '/factura/<int:id>')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
            