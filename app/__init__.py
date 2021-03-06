# __init__.py  Azure Certification

import logging
import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
app.config["TEMPLATES_AUTO_RELOAD"] = True
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')

from app import routes, models, errors