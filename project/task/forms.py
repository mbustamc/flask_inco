from flask_wtf import FlaskForm

from wtforms import StringField, BooleanField, TextAreaField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Length
from project.models import *

from project import db



class TaskForm(FlaskForm):
	area_id = SelectField('Area', coerce=int)
	content = TextAreaField('Task', validators=[Length(min=0, max=300)])
	estado_id = SelectField('Estado', coerce=int)
	submit = SubmitField('Submit')
