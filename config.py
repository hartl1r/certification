# config.py # AzureCertification

import os
import pyodbc
import urllib

from flask import Flask
from dotenv import load_dotenv
from flask_mail import Mail,Message

app = Flask(__name__)

# mail setup
app.config['MAIL_SERVER']='outlook.office365.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USERNAME'] = 'dhartley@thevwc.net'
app.config['MAIL_PASSWORRD'] = 'vwc-0513'
app.config['MAIL_USE_TLS'] = True

# LOAD dotenv IN THE BASE DIRECTORY
basedir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(basedir, '.env')
load_dotenv(dotenv_path)

# print (os.getenv('Driver'))
# print (os.getenv('Server'))
# print (os.getenv('Database'))
# print (os.getenv('Username'))
# print (os.getenv('Password'))
params = urllib.parse.quote_plus('DRIVER=' +  os.getenv('Driver') + ';'
                                    'SERVER=' + os.getenv('Server') + ';'
                                    'DATABASE=' + os.getenv('Database') + ';'
                                    'UID=' + os.getenv('Username') + ';'
                                    'PWD=' + os.getenv('Password') + ';'
)
conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)

class Config(object):
    SQLALCHEMY_DATABASE_URI = conn_str 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD=True 
    SECRET_KEY = os.environ.get('Secret_key')