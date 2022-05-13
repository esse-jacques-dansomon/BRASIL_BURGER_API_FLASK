from flask import Blueprint, request, jsonify

from src.constantes import http_status_code
from src.constantes.url_prefix import PREFIX_URL
from src.models.Burger import Burger
from src.models.Complement import Complement
from src.models.Menu import Menu

menus = Blueprint('menus', __name__, url_prefix=PREFIX_URL + '/menus')


@menus.get('')
def get_all_menus():
    """
    Get all menus
    :return:
    """
    menus = Menu.query.all()
    return jsonify([menu.serialize() for menu in menus]), http_status_code.HTTP_200_OK


@menus.get('/<int:menu_id>')
def get_menu(menu_id):
    """
    Get menu by id
    :param menu_id:
    :return:
    """
    menu = Menu.query.filter_by(id=menu_id).first()
    if menu is None:
        return {
                'data': None,
                'status': http_status_code.HTTP_404_NOT_FOUND,
                'message': 'Menu not found',
                'error': True
            }, http_status_code.HTTP_404_NOT_FOUND
    return menu.serialize(), http_status_code.HTTP_200_OK


@menus.post('')
def create_menu():
    name = request.json.get('name', None)
    description = request.json.get('description', None)
    burger_id = request.json.get('burger_id', None)
    cook_time = request.json.get('cook_time', None)
    complements = request.json.get('complements', None)

    if name is None or description is None or complements is None or cook_time is None or burger_id is None:
        return {'data': [], 'status': 400,
                'message': 'name, description, images or complemets  or cook time are required ',
                'error': True}, http_status_code.HTTP_400_BAD_REQUEST
    burger = Burger.query.filter_by(id=burger_id).first()
    if burger is None:
        return {'data': [], 'status': 404,
                'message': 'Menu doit avoir un burger', 'error': True}, http_status_code.HTTP_404_NOT_FOUND
    price = burger.price
    menu = Menu(name, price, description, cook_time, burger_id)
    mbr_complement = 0
    for complement in complements:
        if complement is not None:
            complement_id = complement['id']
            complement = Complement.query.filter_by(id=complement_id).first()
            if complement is not None:
                menu.price += complement.price
                menu.complements.append(complement)
                mbr_complement += 1
    if mbr_complement == 0:
        return {'data': [], 'status': 404,
                'message': 'Menu doit avoir un Complement', 'error': True}, http_status_code.HTTP_404_NOT_FOUND
    menu.save()
    return menu.serialize(), http_status_code.HTTP_201_CREATED


@menus.put('/<int:menu_id>')
@menus.patch('/<int:menu_id>')
def update_menu(menu_id):
    menu = Menu.query.filter_by(id=menu_id).first()
    if menu is None:
        return {'data': [], 'status': 404, 'message': 'Menu not found',
                'error': True}, http_status_code.HTTP_404_NOT_FOUND
    data = request.get_json(force=True)
    if data is None or data == {}:
        return {'data': [], 'status': 400, 'message': 'No data', 'error': True}, http_status_code.HTTP_400_BAD_REQUEST

    menu.update_product(data)
    complements = request.json.get('complements', None)
    if complements is not None:
        for complement in complements:

            if complement['id'] is not None:
                complement_id = int(complement['id'])
                complement = Complement.query.filter_by(id=complement_id).first()
                if complement is not None and complement.id not in menu.complements:
                    menu.price += complement.price
                    menu.complements.append(complement)
    cook_time = request.json.get('cook_time', None)
    if cook_time is not None:
        menu.cook_time = cook_time
    burger_id = request.json.get('burger_id', None)
    if burger_id is not None:
        burger = Burger.query.filter_by(id=burger_id).first()
        if burger is not None:
            menu.burger_id = burger_id
            menu.price += burger.price
    menu.save()
    menu.update_price()
    return menu.serialize(), http_status_code.HTTP_200_OK
