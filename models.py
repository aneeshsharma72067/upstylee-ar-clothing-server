from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

db = SQLAlchemy()


def get_uuid():
    return uuid4().hex


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, first_name, last_name, email, phone_number, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.password = password


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    category = db.Column(
        db.String(10), nullable=False
    )  # 'men', 'women', 'boys', 'girls'
    type = db.Column(
        db.String(50), nullable=False
    )  # 'shirt', 'jeans', 'jacket', 'kurta', 'pajama', 'shorts', 'top', etc.
    description = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, nullable=True)

    def __init__(
        self,
        name,
        brand,
        category,
        type,
        price,
        description=None,
        rating=None,
        discount=None,
    ):
        self.name = name
        self.brand = brand
        self.category = category
        self.type = type
        self.description = description
        self.rating = rating
        self.price = price
        self.discount = discount
