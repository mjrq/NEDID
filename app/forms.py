from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, IntegerField
from app.models import Provincias, Municipios
from wtforms.validators import DataRequired

class IndexForm(FlaskForm):
    client_id = IntegerField('ID Cliente', [DataRequired(message='Por favor rellene este campo')], default=1)
    provincia = SelectField('Provincia', 
                            choices=[(pro.CPRO, pro.NOMBRE) 
                                    for pro in Provincias.query.order_by('NOMBRE').all()])
    municipio = SelectField('Municipio', choices=[])
    address = StringField('Dirección', [DataRequired(message='Por favor rellene este campo')])
    enviar = SubmitField('Enviar')

class SearchBy(FlaskForm):
    id = StringField('ID', [DataRequired('Por favor rellene este campo')])
    submit = SubmitField()