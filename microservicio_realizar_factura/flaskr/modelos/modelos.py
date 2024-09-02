from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

db = SQLAlchemy()

class Factura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer)
    nombre = db.Column(db.String(128))
    monto = db.Column(db.Float)
    detalle = db.Column(db.String(128))
    estado = db.Column(db.String(128))
    fecha = db.Column(db.DateTime)

class FacturaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Factura
        load_instance = True

    id = fields.Int(dump_only=True)
    usuario_id = fields.Int(required=True)
    nombre = fields.Str(required=True)
    monto = fields.Float(required=True)
    detalle = fields.Str(required=True)
    estado = fields.Str(required=True)
    fecha = fields.DateTime(required=True)