from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate

CONSULTANTS = ['Виктор Петрухин', 'Дарья Аляпина', 'Татьяна Аляпко']
#CONSULTANTS = []
app = Flask(__name__, static_folder='static', static_url_path='/')
app.secret_key = 'My_very_very_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./feedback.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from myapp import models
from myapp import routes

