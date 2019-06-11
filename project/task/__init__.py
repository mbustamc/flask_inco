#task/__init__.py

from flask import Blueprint

bp = Blueprint('task', __name__)

from project.task import routes