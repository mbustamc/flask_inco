#task/__init__.py

from flask import Blueprint

bp = Blueprint('reparacion', __name__)

from project.reparacion import routes