#__init__.py
from flask import Blueprint

bp = Blueprint('admin', __name__)

from project.admin import routes
