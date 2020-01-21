# config.py #

import os
import urllib.parse
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};"
                                 "SERVER={localhost\SQLEXPRESS};"
                                 "UID=sa;"
                                 "PWD={vwc-0513!};"
                                 "DATABASE=woodshop;"
                                 "Persist Security Info=False;"
                                 "MultipleActiveResultSets=False;"
                                 "Encrypt=yes;"
                                 "TrustServerCertificate=yes;"
                                 "Connection timeout=30;")
    conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
    SQLALCHEMY_DATABASE_URI = conn_str 
    #REDIS_URL = "redis://:password@localhost:6379/0"
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #    'sqlite:///' + os.path.join(basedir, 'Woodshop.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']
