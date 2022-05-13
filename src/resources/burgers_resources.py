from flask import Blueprint, jsonify, request

from src.constantes import http_status_code
from src.constantes.url_prefix import PREFIX_URL
from src.models.Menu import Menu
from src.models.Burger import Burger
from src.services.lib import is_granted

burgers = Blueprint('burgers', __name__, url_prefix='/burgers', )


@burgers.get('')
def get_burgers():
    burgers = Burger.query.all()
    burgers_list = [burger.serialize() for burger in burgers]
    return jsonify(burgers_list), http_status_code.HTTP_200_OK


@burgers.post('')
def post_burgers():
    name = request.json.get('name', None)
    price = request.json.get('price', None)
    description = request.json.get('description', None)
    cook_time = request.json.get('cook_time', None)
    if name is None or description is None or price is None or cook_time is None:
        return {'data': [], 'status': 400,
                'message': 'name, description, images or complemets  or cook time are required ',
                'error': True}, http_status_code.HTTP_400_BAD_REQUEST
    burger = Burger(name, price, description, cook_time)
    burger.save()
    return burger.serialize(), http_status_code.HTTP_201_CREATED


@burgers.patch('/edit')
def delete_burger():
    id = request.json.get('id', None)
    is_popular = request.json.get('is_popular', None)
    is_available = request.json.get('is_available', None)
    is_featured = request.json.get('is_featured', None)
    is_offer_of_the_day = request.json.get('is_offer_of_the_day', None)
    burger = Burger.query.filter_by(id=id).first()
    if burger:
        burger.is_available = bool(is_available)
        burger.is_popular = bool(is_popular)
        burger.is_featured = bool(is_featured)
        burger.is_offer_of_the_day = bool(is_offer_of_the_day)
        burger.save()
        return burger.serialize(), http_status_code.HTTP_200_OK
    else:
        return {'data': [], 'status': 404, 'message': 'Not found', 'error': True}, http_status_code.HTTP_404_NOT_FOUND


@burgers.get('/<id>')
def get_burger(id):
    burger = Burger.query.filter_by(id=id).first()
    if burger:
        return burger.serialize(), http_status_code.HTTP_200_OK
    else:
        return {'data': [], 'status': 404, 'message': 'Not found', 'error': True}, http_status_code.HTTP_404_NOT_FOUND


@burgers.put('/<id>')
@burgers.patch('/<id>')
@is_granted('ROLE_ADMIN')
def update_burger(id):
    burger = Burger.query.filter_by(id=id).first()
    if burger:
        data = request.get_json(force=True)
        burger.update_product(data)
        if 'cook_time' in data:
            burger.cook_time = data['cook_time']
        burger.save()
        # update menus that cntains this burger
        menus = Menu.query.filter_by(burger_id=id).all()
        if menus:
            for menu in menus:
                menu.update_price()
                menu.save()
        return burger.serialize(), http_status_code.HTTP_200_OK
    else:
        return {'data': [], 'status': 404, 'message': 'Not found', 'error': True}, http_status_code.HTTP_404_NOT_FOUND
