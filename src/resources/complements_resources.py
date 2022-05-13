from flask import Blueprint, request, jsonify

from src.constantes import http_status_code
from src.constantes.url_prefix import PREFIX_URL
from src.models.Complement import Complement
from src.models.ComplementType import ComplementType

complements = Blueprint('complements', __name__, url_prefix=PREFIX_URL + '/complements')


@complements.get('')
def get_complements():
    """
    Get all complements
    :return:
    """
    complements_list = [complement.serialize() for complement in Complement.query.all()]
    return jsonify(complements_list), http_status_code.HTTP_200_OK


@complements.get('/<id>')
def get_complement(id):
    """
    Get a complement
    :param id:
    :return:
    """
    complement = Complement.query.filter_by(id=id).first()
    if complement is None:
        return {'data': [], 'status': 404, 'message': 'Complement not found',
                'error': True}, http_status_code.HTTP_404_NOT_FOUND
    return complement.serialize(), http_status_code.HTTP_200_OK


@complements.post('')
def create_complement():
    """
    Create a complement
    :return:
    """
    data = request.get_json(force=True)
    name = request.json.get('name', None)
    price = request.json.get('price', None)
    description = request.json.get('description', None)
    type_id = data['type_id']
    if type_id is None or ComplementType.query.filter_by(id=type_id).first() is None:
        return {'data': [], 'status': 404,
                'message': 'complement doit avoir un type'}, http_status_code.HTTP_404_NOT_FOUND
    if name is None or price is None or description is None:
        return {'data': [], 'status': 400,
                'message': 'name, price, description  are required'}, http_status_code.HTTP_400_BAD_REQUEST
    complement = Complement(name, price, description, type_id)
    complement.save()
    return complement.serialize(), http_status_code.HTTP_201_CREATED


@complements.put('/<id>')
@complements.patch('/<id>')
def update_complement(id):
    complement = Complement.query.filter_by(id=id).first()
    if complement:
        data = request.get_json(force=True)
        complement.update_product(data)
        complement.save()
        # update menus that cntains this complement
        menus = complement.menus
        if menus:
            for menu in menus:
                menu.update_price()
                menu.save()
        complement.save()
        return complement.serialize(), http_status_code.HTTP_200_OK
    else:
        return {'data': [], 'status': 404, 'message': 'Not found', 'error': True}, http_status_code.HTTP_404_NOT_FOUND
