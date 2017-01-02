from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Config
app = Flask(__name__)
app.config.from_object('config')

# Extensions
db = SQLAlchemy(app)

from project import views, models
from project.models import User
