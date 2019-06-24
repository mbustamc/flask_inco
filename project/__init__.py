from flask import Flask
from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import flask_excel as excel

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from flask_login import LoginManager


db = SQLAlchemy()
login = LoginManager()
fl_admin = Admin(name='Template!', template_mode='bootstrap3')

def create_app():

	application = Flask(__name__)
	application.config.from_object(Config)

	excel.init_excel(application)
	db.init_app(application)
	migrate = Migrate(application, db)
	
	fl_admin.init_app(application)

	login.init_app(application)
	login.login_message = 'You must be logged in to access this page.'
	login.login_view = 'auth.login'
	

	from project import models

	from project.main import bp as main
	application.register_blueprint(main)

	from project.task import bp as task
	application.register_blueprint(task, url_prefix='/task')

	from project.auth import bp as auth
	application.register_blueprint(auth, url_prefix='/auth')

	from project.admin import bp as admin_bp
	application.register_blueprint(admin_bp)

	from project.errors import bp as errors
	application.register_blueprint(errors)
	


		
	return application