from flask_wtf import FlaskForm

from wtforms import StringField, BooleanField, TextAreaField, SubmitField, SelectField, DateField, validators
from wtforms.validators import ValidationError, DataRequired, Length
from project.models import *

from wtforms.fields.html5 import DateField
from project import db



class ReparacionForm(FlaskForm):
	maquina_id = SelectField('Maquina', coerce=int)
	content = TextAreaField('Reparacion', validators=[Length(min=0, max=300)])
	created = DateField(u'Creacion (dd-mm-aaaa)', format='%d-%m-%Y')
	submit = SubmitField('Submit')
