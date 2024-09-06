from flaskr import create_app
from .modelos import db, Usuario
from flask_restful import Api
from .vistas import VistaUsuarios, VistaUsuario

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaUsuarios, '/usuarios')
api.add_resource(VistaUsuario, '/usuario/<int:id>')

with app.app_context():
    usuario1 = Usuario(nombre='Luis Alejandro Bogota', correo='l.bogotab@uniandes.edu.co', canal_comunicacion='Chat', PQR=6)
    usuario2 = Usuario(nombre='Romel Alejandro', correo='romel.uniandes.edu.co', canal_comunicacion='Correo', PQR=3)

    db.session.add(usuario1)
    db.session.add(usuario2)
    db.session.commit()
