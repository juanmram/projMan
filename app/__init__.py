import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

#Create an Instance of Flask
app = Flask(__name__, instance_relative_config=True)

#Include config from config.py
app.config.from_object('config')
#app.config.from_pyfile('config.py')
app.secret_key = '\xa6\x8f\xb8d\x00\xdaH\xd2i\x96\xc9v0$]:\xae\xdb\xd3\xd9k\xa2\xe5\x9a'

login_manager = LoginManager()
db = SQLAlchemy()

#Create an instance of SQLAclhemy
login_manager.init_app(app)
db.init_app(app)
bootstrap = Bootstrap(app)

from app import views, models
