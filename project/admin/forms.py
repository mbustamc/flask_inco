#app/admin/forms.py
from flask_wtf import Form
from wtforms import StringField, IntegerField, SubmitField, validators, SelectField

from project.models import *

#from app import db
#from app.mod_catalogo.models import Category

class AreaForm(Form):
    name = StringField('Nombre Area')
    submit = SubmitField('Enviar')


class MaquinasForm(Form):
    name = StringField('Nombre Area')
    area = SelectField(u'Selecciona Area', choices=[])
    submit = SubmitField('Enviar')
