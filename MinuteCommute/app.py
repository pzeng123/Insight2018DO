from flask import Flask
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('local_settings.py', silent=True)

Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

# app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Listing
db.create_all()