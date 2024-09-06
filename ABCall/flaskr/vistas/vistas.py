from flask_restful import Resource
from ..modelos import db, Usuario, UsuarioSchema
from flask import request, jsonify
from datetime import datetime
from celery import Celery

celery_app = Celery(__name__, broker='redis://redis:6379/0')

@celery_app.task(name='registrar_log')
def registrar_log(*args):
    pass

usuario_schema = UsuarioSchema(many=True)
usuario_single_schema = UsuarioSchema()


class VistaUsuarios(Resource):
    
        def get(self):
            usuarios = Usuario.query.all()
            return usuario_schema.dump(usuarios), 200
        
        def post(self):
            usuario_data = request.json
            usuario = usuario_single_schema.load(usuario_data, session=db.session)
            db.session.add(usuario)
            db.session.commit()
            args = ('Registro', datetime.now().isoformat())
            registrar_log.apply_async(args=args, queue='logs')
            return usuario_single_schema.dump(usuario), 201

class VistaUsuario(Resource):
        
        def get(self, id):
            usuario = Usuario.query.get_or_404(id)
            return usuario_single_schema.dump(usuario), 200
            
        def put(self, id):
            usuario = Usuario.query.get_or_404(id)
            usuario_data = request.json
            usuario = usuario_single_schema.load(usuario_data, instance=usuario, session=db.session)
            db.session.commit()
            return usuario_single_schema.dump(usuario), 200
            
        def delete(self, id):
            usuario = Usuario.query.get_or_404(id)
            db.session.delete(usuario)
            db.session.commit()
            return '', 204