import os
from bbs.setting import *
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))


db = SQLAlchemy(app)
migrate = Migrate(app, db)