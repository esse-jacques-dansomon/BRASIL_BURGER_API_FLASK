from flask import Blueprint, jsonify, request

from src.constantes import http_status_code
from src.constantes.url_prefix import PREFIX_URL
from src.models.Product import Product

products = Blueprint('products', __name__, url_prefix=PREFIX_URL + '/products')


@products.get('')
def get_products():
    try:
        products = Product.query.all()
        return jsonify([product.serialize() for product in products]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@products.get('/complements')
def get_complements():
    try:
        products = Product.query.filter_by(product_type='complement').all()
        return jsonify([product.serialize() for product in products]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@products.get('/menus')
def get_menu_products():
    try:
        products = Product.query.filter_by(product_type='menu').all()
        return jsonify([product.serialize() for product in products]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@products.patch('/edit')
def delete_burger():
    id = request.json.get('id', None)
    is_popular = request.json.get('is_popular', None)
    is_available = request.json.get('is_available', None)
    is_featured = request.json.get('is_featured', None)
    is_offer_of_the_day = request.json.get('is_offer_of_the_day', None)
    burger = Product.query.filter_by(id=id).first()
    if burger:
        burger.is_available = bool(is_available)
        burger.is_popular = bool(is_popular)
        burger.is_featured = bool(is_featured)
        burger.is_offer_of_the_day = bool(is_offer_of_the_day)
        burger.save()
        return burger.serialize(), http_status_code.HTTP_200_OK
    else:
        return {'data': [], 'status': 404, 'message': 'Not found', 'error': True}, http_status_code.HTTP_404_NOT_FOUND


@products.get('/popular')
def get_popular_products():
    try:
        products = Product.query.filter_by(is_popular=True).all()
        return jsonify([product.serialize() for product in products]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@products.get('/menu_of_the_day')
def get_menu_of_the_day():
    try:
        products = Product.query.filter_by(is_offer_of_the_day=True).all()
        return jsonify([product.serialize() for product in products]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@products.get('/featured')
def get_featured_products():
    try:
        products = Product.query.filter_by(is_featured=True).all()
        return jsonify([product.serialize() for product in products]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
