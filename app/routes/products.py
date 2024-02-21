from flask import Blueprint

products_bp = Blueprint('products',__name__)

@products_bp.route("/<id>")
def getAllProducts(id):
    return "product"
