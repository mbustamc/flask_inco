from flask_wtf import FlaskForm

from wtforms import StringField, BooleanField, TextAreaField, SubmitField, SelectField, DateField, validators
from wtforms.validators import ValidationError, DataRequired, Length
from project.models import *

from wtforms.fields.html5 import DateField
from project import db

choices_detencion=[
	('10', '10 min'),
	('20', '20 min'), 
	('30', '30 min'),
	('45', '45 min'),
	('60', '1 hr'), 
	('90', '1,5 hrs'),
	('120', '2 hrs'),
	('150', '2,5 hrs'),
	('180', '3 hrs'),
	('210', '3,5 hrs'),
	('240', '4 hrs'),
	('270', '4,5 hrs'),
	]



class ReparacionForm(FlaskForm):
	maquina_id = SelectField('Maquina', coerce=int, validators = [DataRequired()])
	detencion_id= SelectField(
        'Tipo detencion',
        coerce=int, validators = [DataRequired()])
	duracion = SelectField(
        'Duracion detencion', choices = choices_detencion,
         validators = [DataRequired()])
	comentarios = TextAreaField('Comentarios', validators=[Length(min=0, max=300)])
	created = DateField(u'Creacion (dd-mm-aaaa)', format='%Y-%m-%d')
	submit = SubmitField('Submit')
