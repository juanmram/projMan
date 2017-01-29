from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#Create an Instance of Flask
app = Flask(__name__, instance_relative_config=True)

#Include config from config.py
#app.config.from_object('config')
app.config.from_pyfile('config.py')

#Create an instance of SQLAclhemy
db = SQLAlchemy(app)

from app import views, models
