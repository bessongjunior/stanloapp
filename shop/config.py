# -*- encoding: utf-8 -*-
"""
Copyright (c) 2023 - present juniorbesong
"""

import os, random, string
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
# basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig():
    
    SECRET_KEY = os.getenv('SECRET_KEY', None)
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT', None)
    if not SECRET_KEY:
        SECRET_KEY = ''.join(random.choice( string.ascii_lowercase  ) for i in range( 32 ))
    
    if not SECURITY_PASSWORD_SALT:
        SECURITY_PASSWORD_SALT = ''.join(random.choice( string.ascii_lowercase  ) for i in range( 37 ))


    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', None)
    if not JWT_SECRET_KEY:
        JWT_SECRET_KEY = ''.join(random.choice( string.ascii_lowercase  ) for i in range( 32 ))

    GOOGLE_CLIENT_ID     = os.getenv('GITHUB_CLIENT_ID' , None)
    GOOGLE_CLIENT_SECRET = os.getenv('GITHUB_SECRET_KEY', None)

    FACEBOOK_CLIENT_ID     = os.getenv('GITHUB_CLIENT_ID' , None)
    FACEBOOK_CLIENT_SECRET = os.getenv('GITHUB_SECRET_KEY', None)
    
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DB_ENGINE   = os.getenv('DB_ENGINE'   , None)
    DB_USERNAME = os.getenv('DB_USERNAME' , None)
    DB_PASS     = os.getenv('DB_PASS'     , None)
    DB_HOST     = os.getenv('DB_HOST'     , None)
    DB_PORT     = os.getenv('DB_PORT'     , None)
    DB_NAME     = os.getenv('DB_NAME'     , None)

    USE_SQLITE  = True 

    # try to set up a Relational DBMS
    if DB_ENGINE and DB_NAME and DB_USERNAME:

        try:
            
            # Relational DBMS: PSQL, MySql
            SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
                DB_ENGINE,
                DB_USERNAME,
                DB_PASS,
                DB_HOST,
                DB_PORT,
                DB_NAME
            ) 

            USE_SQLITE  = False

        except Exception as e:

            print('> Error: DBMS Exception: ' + str(e) )
            print('> Fallback to SQLite ')    

    if USE_SQLITE:

        # This will create a file in <app> FOLDER
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'platformdb.sqlite3')

    UPLOADED_PHOTOS_DEST = os.path.join(BASE_DIR, 'static/images')  #os.path.join(basedir, 'static/images')
    MAIL_SERVER = 'smtp.gmail.com' #'smtp.googlemail.com'
    MAIL_PORT = 587#,465  
    MAIL_USE_TLS= True
    MAIL_USERNAME = 'juniorbesong8@gmail.com' #os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = 'rmni qoyl glsc zjzu' #os.environ.get('EMAIL_PASS')
    MAIL_USE_TLS= True#False
    MAIL_USE_SSL= False#True