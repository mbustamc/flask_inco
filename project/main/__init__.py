#bp_mani/__init__.py

from flask import Blueprint

bp = Blueprint('main', __name__)

from project.main import routes