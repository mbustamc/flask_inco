#admin/__init__.py

from flask import Blueprint

bp = Blueprint('admin_bp', __name__)

from project.admin import routes