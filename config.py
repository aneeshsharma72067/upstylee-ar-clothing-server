from dotenv import load_dotenv
from os import environ  

load_dotenv()

class ApplicationConfig:
    SECRET_KEY = environ['SECRET_KEY']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = r"sqlite:///./db.sqlite"
    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = False
    SESSION_USER_SIGNER = True
    DEBUG = True
    FLASK_ENV = 'development'