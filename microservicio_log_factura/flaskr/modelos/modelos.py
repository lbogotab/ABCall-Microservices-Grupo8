from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

db = SQLAlchemy()

class Factura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128))
    monto = db.Column(db.Float)
    estado = db.Column(db.String(128))
    fecha = db.Column(db.DateTime)

class FacturaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Factura
        load_instance = True

    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    monto = fields.Float(required=True)
    estado = fields.Str(required=True)
    fecha = fields.DateTime(required=True)