from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#Create an Instance of Flask
app = Flask(__name__)

#Include config from config.py
app.config.from_object('config')
app.secret_key = 'dfdffvfdvfd441445!=sdc'

#Create an instance of SQLAclhemy
db = SQLAlchemy(app)

from app import views, models
