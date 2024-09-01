from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128))
    correo = db.Column(db.String(128))
    canal_comunicacion = db.Column(db.String(128))
    PQR = db.Column(db.Integer)

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True

    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    correo = fields.Str(required=True)
    canal_comunicacion = fields.Str(required=True)
    PQR = fields.Int(required=True)

