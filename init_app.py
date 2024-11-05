from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy

print('start init')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myfirstdb.db'
db = SQLAlchemy(app)
admin = Admin(app, name='My Admin Panel', template_mode='bootstrap3')
print('stop init')
