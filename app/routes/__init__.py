from flask import Flask
from .auth import auth_bp
from .users import users_bp
from .products import products_bp

def register_routes(app:Flask):
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(products_bp, url_prefix='/api/products')