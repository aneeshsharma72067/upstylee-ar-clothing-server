from flask import Flask
from flask_cors import CORS
from app.models.models import db
from config import ApplicationConfig
from flask_bcrypt import Bcrypt
from flask_session import Session
from app.routes import register_routes

app = Flask(__name__)
app.config.from_object(ApplicationConfig)

# Initialise Extensions
bcrypt = Bcrypt(app)
server_session = Session(app)
db.init_app(app)
CORS(app)

# Import and Register Routes
register_routes(app)

#Create all database tables
with app.app_context():
    db.create_all()

