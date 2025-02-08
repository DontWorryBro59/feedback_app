from flask import Flask
CONSULTANTS = ['Виктор Петрухин', 'Дарья Аляпина', 'Татьяна Аляпко']
#CONSULTANTS = []
app = Flask(__name__, static_folder='static', static_url_path='/')
app.secret_key = 'My_very_very_secret_key'

from myapp import models
from myapp import routes

