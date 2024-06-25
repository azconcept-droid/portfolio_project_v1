#!myvenv/bin/python3
"""Initializes the Flask app"""

from flask import Flask
from config import Config
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

from frontend import index
from models import agent, customer
