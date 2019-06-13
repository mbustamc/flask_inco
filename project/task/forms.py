from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Length
from project.models import *



class TaskForm(FlaskForm):
    area = SelectField('Area', choices=[('env', 'Envasado'), ('elab', 'Elaboracion'), ('tur', 'Turbinas'),  ('var', 'Otros')])
    content = TextAreaField('Task', validators=[Length(min=0, max=300)])
    submit = SubmitField('Submit')
