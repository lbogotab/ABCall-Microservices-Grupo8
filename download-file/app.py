import requests
from flask import Flask, jsonify
from flask_restful import Api, Resource
from celery import Celery
from datetime import datetime

app = Flask(__name__)
api = Api(app)

celery_app = Celery('tasks', broker='redis://localhost:6379/0')


@celery_app.task(name='descarga_factura_log')
def registrar_log_descarga(id_factura, fecha_descarga):
    print(f"Log registrado para la descarga de la factura {id_factura} en {fecha_descarga}")


class VistaDescargarFactura(Resource):
    def get(self, id):
        response = requests.get(f'http://localhost:5061/factura/{id}')

        if response.status_code == 404:
            return {'message': 'Factura no encontrada'}, 404

        factura = response.json()

        factura_descargada = {
            'usuario_id': factura['usuario_id'],
            'nombre': factura['nombre'],
            'monto': factura['monto'],
            'detalle': f"Factura descargada para {factura['detalle'].split(' ')[-1]}",
            'estado': 'Descargada',
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        registrar_log_descarga.delay(factura_descargada['usuario_id'], factura_descargada['fecha'])

        return jsonify(factura_descargada)


api.add_resource(VistaDescargarFactura, '/descargar_factura/<int:id>')

@app.route("/health")
def health():
    return "Download file está ok!"


if __name__ == '__main__':
    app.run(debug=True, port=5063)
