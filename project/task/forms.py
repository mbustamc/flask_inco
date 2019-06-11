from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length
from project.models import Task


class TaskForm(FlaskForm):
    content = TextAreaField('Task', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
