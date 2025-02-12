import os, datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, static_folder='static', static_url_path='/')
app.secret_key = os.urandom(20).hex()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./feedback.db'
app.config['CONSULTANTS'] = []
app.config['SEND_FLAG'] = False
app.config['pass_adm_def'] = 'admin'
app.config['session_time'] = datetime.timedelta(seconds=300)
app.config['session_permanent'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from myapp import models
from myapp import routes


with app.app_context():
    # При инициализации приложения получаем данные из БД и создаем переменную CONSULTANTS
    consults = db.session.query(models.Workers).all()
    for el in consults:
        app.config['CONSULTANTS'].append(el.full_name)
    # Добавляем в базу данных базового администратора
    admins = db.session.query(models.Admins).all()
    if not admins:
        new_admin = models.Admins(username='admin')
        new_admin.set_password(app.config['pass_adm_def'])
        db.session.add(new_admin)
        db.session.commit()
