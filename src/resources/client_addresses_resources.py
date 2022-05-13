from flask import Blueprint, jsonify, request

from src.constantes import http_status_code
from src.constantes.url_prefix import PREFIX_URL
from src.models.Address import Address, get_all_by_client
from src.services.lib import is_granted, getUser

addresses = Blueprint('addresses', __name__, url_prefix=PREFIX_URL + '/addresses')


@addresses.get('/client/<int:id>')
@is_granted('ROLE_USER')
def get_addresses(id):
    client = getUser()
    if client.id != id:
        return jsonify({'message': 'You are not allowed to access this resource'}), http_status_code.HTTP_403_FORBIDDEN
    addresses = [adresse.serialize() for adresse in get_all_by_client(client_id=client.id)]
    return jsonify(
        {'data': addresses, 'status': 200, 'message': 'success', 'error': False}), http_status_code.HTTP_200_OK


@addresses.post('')
@is_granted('ROLE_USER')
def create_address():
    street = request.json.get('street', None)
    city = request.json.get('city', None)
    state = request.json.get('state', None)
    if street is None or city is None:
        return jsonify({'message': 'Missing parameters'}), http_status_code.HTTP_400_BAD_REQUEST
    client = getUser()
    adresse = Address(street, city, state, client.id)
    adresse.save()
    return jsonify({'data': [adresse.serialize()], 'status': 201, 'message': 'created',
                    'error': False}), http_status_code.HTTP_201_CREATED


@addresses.put('/<int:id>')
@addresses.patch('/<int:id>')
@is_granted('ROLE_USER')
def update_address(id):
    client, address = getUser(), Address.query.filter_by(id=id).first()
    if address is None or client is None or client.id != address.client_id:
        return jsonify({'message': 'You are not allowed to access this resource'}), http_status_code.HTTP_403_FORBIDDEN
    address.update(request.get_json(force=True))
    return jsonify({'data': [address.serialize()], 'status': 200, 'message': 'updated',
                    'error': False}), http_status_code.HTTP_200_OK


@addresses.delete('/<int:id>')
@is_granted('ROLE_USER')
def delete_addresse(id):
    client, address = getUser(), Address.query.filter_by(id=id).first()
    if address is None or client is None or client.id != address.client_id:
        return jsonify({'message': 'You are not allowed to access this resource'}), http_status_code.HTTP_403_FORBIDDEN
    address.delete()
    return jsonify({'data': [address.serialize()], 'status': 200, 'message': 'deleted',
                    'error': False}), http_status_code.HTTP_200_OK
