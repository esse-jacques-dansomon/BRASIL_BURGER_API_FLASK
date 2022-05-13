import os
import uuid

from flask import Blueprint, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename

from src.constantes.http_status_code import HTTP_200_OK, HTTP_400_BAD_REQUEST
from src.constantes.url_prefix import PREFIX_URL
from src.models.ComplementType import ComplementType
from src.models.Product import Product

images = Blueprint('images', __name__, url_prefix=PREFIX_URL + '/images')


@images.put('/<id>')
@images.patch('/<id>')
def upload(id):
    product = Product.query.get(id)
    if product is None:
        return jsonify({'message': 'Product not found'}), HTTP_400_BAD_REQUEST
    if 'file' not in request.files:
        return jsonify({'error': "No file part in the request"}), HTTP_400_BAD_REQUEST
    else:
        uploadImage(product, request)



def uploadImage(product, request):
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': "No file selected for uploading"}), HTTP_400_BAD_REQUEST
    if file:
        filename = secure_filename(file.filename)
        unique_filename = str(uuid.uuid4()) + '.' + filename.rsplit('.', 1)[1]
        file.save(os.path.join('src/static/images', unique_filename))
        product.image = unique_filename
        product.update()
        return jsonify({'message': "File successfully uploaded", 'path': unique_filename}), HTTP_200_OK
    return jsonify({'error': "Allowed file types are txt, pdf, png, jpg, jpeg, gif"}), HTTP_400_BAD_REQUEST
