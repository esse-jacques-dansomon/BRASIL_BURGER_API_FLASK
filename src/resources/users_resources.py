
from flask import Blueprint

from src.constantes.url_prefix import PREFIX_URL
from src.models.User import User

users = Blueprint('userResource', __name__, url_prefix=PREFIX_URL + '/users')


@users.get('/')
def create_user():
    return {'data': [user.serialize() for user in User.query.all()], 'message': 'List of users'}, 200
