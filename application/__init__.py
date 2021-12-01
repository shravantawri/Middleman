from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://middleman@localhost/middleman_development"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['QR_CODE_FOLDER'] = 'application/static/images'


db = SQLAlchemy()

from application import routes
from application import models

db.init_app(app)