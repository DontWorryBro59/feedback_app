from flask import Flask

app = Flask(__name__, static_folder='static', static_url_path='/')


from myapp import models
from myapp import routes