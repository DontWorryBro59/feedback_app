from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

CONSULTANTS = []
app = Flask(__name__, static_folder='static', static_url_path='/')
app.secret_key = 'My_very_very_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./feedback.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from myapp import models
from myapp import routes

# При инициализации приложения получаем данные из БД и создаем переменную CONSULTANTS
with app.app_context():
    consults = db.session.query(models.Workers).all()
    for el in consults:
        CONSULTANTS.append(el.full_name)


class AdminConfig:

    def __init__(self):
        self.consultants = []
        self.admin_login = 'admin'
        self.admin_password = '123pass456!'
        self.admin_login_def = 'admin'
        self.admin_password_def = '123pass456!'
        self.start_send = True

admin_config = AdminConfig()