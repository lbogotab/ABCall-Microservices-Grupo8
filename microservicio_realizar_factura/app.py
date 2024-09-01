from datetime import datetime
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import requests

def create_app(config_name):
    app = Flask(__name__)
    return app

app = create_app('default')
app_context = app.app_context()
app_context.push()

api = Api(app)

class VistaRealizarFactura(Resource):
    def post(self, id):
        response = requests.get(f'http://localhost:5000/usuario/{id}')
        
        if response.status_code == 404:
            return response.json(), 404
        else:
            usuario = response.json()
            factura = self.realizar_factura(usuario)
            return jsonify(factura)

    def realizar_factura(self, usuario):
        pqr = usuario.get('PQR', 0)
        canal_comunicacion = usuario.get('canal_comunicacion')

        multiplicadores = {
            'Chat': 10,
            'Correo': 20,
            'Llamada': 30
        }

        monto = pqr * multiplicadores.get(canal_comunicacion, 1)

        factura = {
            'usuario_id': usuario['id'],
            'nombre': usuario['nombre'],
            'monto': monto,
            'detalle': f'Factura generada para {canal_comunicacion}',
            'estado': 'Pendiente',
            'fecha': datetime.now().isoformat()
        }
        return factura

api.add_resource(VistaRealizarFactura, '/realizar_factura/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
            