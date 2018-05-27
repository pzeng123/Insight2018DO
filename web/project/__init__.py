#################
##        imports 

import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy





################
##        config 


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('local_settings.py', silent=True)

Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

