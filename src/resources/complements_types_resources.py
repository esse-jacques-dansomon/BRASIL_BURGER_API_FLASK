from flask import Blueprint, request, jsonify

from src.constantes import http_status_code
from src.constantes.url_prefix import PREFIX_URL
from src.models.ComplementType import ComplementType
from src.services import file_uploader

complements_types = Blueprint('complements_types', __name__, url_prefix=PREFIX_URL + '/complements_types')


@complements_types.get('')
def get_complements_types():
    complements_list = [complement.serialize() for complement in ComplementType.query.all()]
    return jsonify(complements_list), http_status_code.HTTP_200_OK


@complements_types.get('/<id>')
def get_complement_type(id):
    complement = ComplementType.query.get(id)
    if not complement:
        return {'data': [], 'status': 404, 'error': True, 'message': 'Errors'}, 404
    return complement.serialize(), 200


@complements_types.post('')
def create_complement_type():
    data = request.get_json(force=True)
    if not data:
        return {'data': [], 'status': 400, 'error': True, 'message': 'errors'}, 400
    if data.get('name'):
        complements_type = ComplementType(name=data.get('name'), image='', description='')
        if data.get('description') or data.get('image'):
            complements_type.description = data.get('description')
            complements_type.image = data.get('image')
        complements_type.save()
        return complements_type.serialize(), 201
    return {'data': [], 'status': 400, 'error': True, 'message': 'errors'}, 400


@complements_types.put('/<id>')
@complements_types.patch('/<id>')
def update_complement_type(id):
    data = request.get_json(force=True)
    if not data:
        return {'data': [], 'status': 400, 'error': True, 'message': 'errors'}, 400
    complement = ComplementType.query.get(id)
    if not complement:
        return {'data': [], 'status': 404, 'error': True, 'message': 'errors'}, 404
    if data.get('name'):
        complement.name = data.get('name')
        complement.slug = complement.slugify(complement.name)
    if data.get('description'):
        complement.description = data.get('description')
    complement.save()
    return complement.serialize(), 200


@complements_types.post('create-teste')
def create_with_file():
    name = request.form.get('name')
    name1 = request.json.get('name')
    return name1, 201
    description = request.form.get('description')
    image = file_uploader.uploadImage(request)
    typeComplement = ComplementType(name=name, description=description, image=image)
    typeComplement.save()
    return typeComplement.serialize(), 201
