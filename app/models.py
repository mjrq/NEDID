from flask import current_app as app
from app import db
from flask_marshmallow import Marshmallow
from datetime import datetime

ma = Marshmallow(app)

# =============================================================================
# CREATE TABLE IF NOT EXIST
# =============================================================================

class Request(db.Model):
    ''' Create the requests Table if it doesn't exists '''
    __tablename__ = 'requests'
    # Columns for the table
    request_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, nullable=False)
    provincia = db.Column(db.String(100), nullable=False)
    municipio = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    init_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)
    req_status = db.Column(db.Integer, nullable=False)
    tipo_via = db.Column(db.String(20), nullable=True)
    nombre_via = db.Column(db.String(100), nullable=True)

    def __init__(self, client_id, provincia, municipio, address,):
        self.client_id = client_id
        self.address = address
        self.provincia = provincia
        self.municipio = municipio
        self.init_date = datetime.now()
        self.req_status = 0
        self.tipo_via = None
        self.nombre_via = None

    def completed_search(self, status, tvia, nvia):
        self.req_status = status
        self.end_date = datetime.now()
        self.tipo_via = tvia
        self.nombre_via = nvia

        
class Municipios(db.Model):
    __tablename__ = 'municipios'
    CAUTO = db.Column(db.String(2), primary_key=True)
    CPRO = db.Column(db.String(2), primary_key=True)
    CMUN = db.Column(db.String(2), primary_key=True)
    DC = db.Column(db.Text, primary_key=True)
    NOMBRE = db.Column(db.Text, nullable=True)


class Provincias(db.Model):
    __tablename__ = 'provincias'
    CPRO = db.Column(db.String(2), primary_key=True)
    NOMBRE = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return '{}'.format(self.NOMBRE)


class Vias(db.Model):
    __tablename__ = 'vias'
    CPRO = db.Column(db.Text, primary_key=True)
    CMUN = db.Column(db.Text, primary_key=True)
    CVIA = db.Column(db.Text, primary_key=True)
    NTVIA = db.Column(db.Text)
    NVIAC = db.Column(db.Text)
    NTVIA_NVIAC = db.Column(db.String(100))


# =============================================================================
# SCHEMA TASKS
# =============================================================================
class RequestSchema(ma.Schema):
    ''' Manage the schema of requests table '''
    class Meta:
        fields = ('request_id',
                  'client_id',
                  'provincia',
                  'municipio',
                  'address',
                  'init_date',
                  'end_date',
                  'req_status',
                  'tipo_via',
                  'nombre_via')
