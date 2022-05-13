from flask import Blueprint, request
from flask_jwt_extended import create_refresh_token, create_access_token
from werkzeug.security import generate_password_hash

from src.constantes.http_status_code import HTTP_200_OK
from src.services import lib
from src.services.Validator import validator_data
from src.constantes import http_status_code
from src.constantes.url_prefix import PREFIX_URL
from src.models.Client import Client

clients = Blueprint('clients', __name__, url_prefix=PREFIX_URL + '/clients')


@clients.get('')
def get_clients():
    clients = [client.serialize() for client in Client.query.all()]
    return {'data': clients if clients else []}, 200 if clients else 404


@clients.get('/<int:id>')
def get_client(id):
    client = Client.query.get(id)
    if client:
        return {'data': [client.serialize()], 'status': 200, 'error': False}, http_status_code.HTTP_200_OK
    return {'data': ['Client not found'], 'status': 404, 'error': True}, http_status_code.HTTP_404_NOT_FOUND


@clients.post('')
def create_client():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    email = request.json.get("email", None)
    phone = request.json.get("phone", None)
    print(username, password, email, phone)
    # validate data
    validator = validator_data()
    validator.empty_validator(username)
    validator.empty_validator(password)
    validator.validate_email(email)
    validator.senegal_number_validator(phone)
    if validator.is_validated():
        password_hash = generate_password_hash(password)
        client = Client(username, password_hash, email, phone)
        client.save()
        refresh = create_refresh_token(identity=client.id)
        access = create_access_token(identity=client.id)
        data = {
            'user': client.serialize(),
            'refresh': str(refresh),
            'access': str(access)
        }
        return data, HTTP_200_OK
    print(validator.errors)
    return {'message': validator.get_errors(), 'status': 400, 'error': True}, http_status_code.HTTP_400_BAD_REQUEST


@clients.put('/<int:id>')
@clients.patch('/<int:id>')
def update_client(id):
    client = Client.query.get(id)
    if client:
        username = request.json.get('username', None)
        email = request.json.get('email', None)
        phone = request.json.get('phone', None)
        client.username = username
        client.email = email
        client.phone = phone
        if client.save():
            return {'data': [client.serialize()] , 'status': 200, 'error': False}, http_status_code.HTTP_200_OK
    return {'data': 'Client not found', 'status': 404, 'error': True}, http_status_code.HTTP_404_NOT_FOUND


@clients.delete('<int:id>')
def delete_client(id):
    client = Client.query.get(id)
    if client:
        if client.delete():
            return {'data': ['Client deleted'], 'status': 200, 'error': False}, http_status_code.HTTP_200_OK
    return {'data': ['Client not found'], 'status': 404, 'error': True}, http_status_code.HTTP_404_NOT_FOUND
