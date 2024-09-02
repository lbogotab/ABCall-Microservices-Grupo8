from flaskr import create_app
from flask_restful import Api, Resource
from .modelos import db, Factura, FacturaSchema

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

factura_schema = FacturaSchema()

class VistaLogFacturas(Resource):
    def get(self):
        facturas = Factura.query.all()
        return [factura_schema.dump(factura) for factura in facturas]

api = Api(app)
api.add_resource(VistaLogFacturas, '/facturaslog')

if __name__ == '__main__':
    app.run(debug=True, port=5002)