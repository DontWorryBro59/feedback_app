import os, datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#from flask_login import LoginManager


app = Flask(__name__, static_folder='static', static_url_path='/')
app.secret_key = os.urandom(20).hex()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./feedback.db'

app.config['CONSULTANTS'] = []
app.config['SEND_FLAG'] = False
app.config['pass_adm_def'] = '123pass456!'
app.config['login_adm'] = 'admin'
app.config['pass_adm'] = '123pass456!'
app.config['session_time'] = datetime.timedelta(seconds=300)
app.config['session_permanent'] = True

#log_manager = LoginManager()
#log_manager.login_view('admin')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from myapp import models
from myapp import routes

# При инициализации приложения получаем данные из БД и создаем переменную CONSULTANTS
with app.app_context():
    consults = db.session.query(models.Workers).all()
    for el in consults:
        app.config['CONSULTANTS'].append(el.full_name)


