import os
from flask import Flask
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app import env

app = Flask(__name__)

# SQL Alchemy and SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# MongoDB Connection Config
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)

from app import routes
