from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from logger import setup_logging

logger = setup_logging(log_file_path='./logs/init.log', logger_name='init_logs')

logger.info('start init')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myfirstdb.db'
db = SQLAlchemy(app)
admin = Admin(app, name='My Admin Panel', template_mode='bootstrap3')
logger.info('stop init')
login_manager = LoginManager(app)
login_manager.login_view = 'login'
