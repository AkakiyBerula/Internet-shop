from flask import Blueprint

products_blueprint = Blueprint('products', __name__, template_folder="templates/products")

from . import views