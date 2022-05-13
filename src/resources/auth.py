from src.constantes.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, \
    HTTP_409_CONFLICT
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity

from src.constantes.url_prefix import PREFIX_URL
from src.models.Database import db
from src.models.User import User
from src.services.lib import is_granted

auth = Blueprint("auth", __name__, url_prefix=PREFIX_URL + "/auth")


@auth.post('/register')
# @swag_from('./docs/auth/register.yaml')
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    if len(password) < 6:
        return jsonify({'error': "Password is too short"}), 201

    if len(username) < 3:
        return jsonify({'error': "User is too short"}), HTTP_400_BAD_REQUEST

    if not username.isalnum() or " " in username:
        return jsonify({'error': "Username should be alphanumeric, also no spaces"}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error': "Email is not valid"}), HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error': "Email is taken"}), HTTP_409_CONFLICT

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error': "username is taken"}), HTTP_409_CONFLICT

    pwd_hash = generate_password_hash(password)
    user = User(username=username, password=pwd_hash, email=email)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': "User created",
        'user': {
            'username': username, "email": email
        }

    }), HTTP_201_CREATED


@auth.post('/login')
# @swag_from('./docs/auth/login.yaml')
def login():
    email = request.json.get('login', '')
    password = request.json.get('password', '')
    print(email, password)
    if not email or not password:
        return jsonify({'error': "Missing credentials"}), HTTP_400_BAD_REQUEST
    user = User.query.filter_by(email=email).first()
    if user:
        is_pass_correct = check_password_hash(user.password, password)
        if is_pass_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)

            data = {
                'user': user.serialize(),
                'refresh': str(refresh),
                'access': str(access)
            }

            return data, HTTP_200_OK

    return jsonify({'error': 'Wrong credentials'}), HTTP_400_BAD_REQUEST


@auth.get("/me")
@is_granted("ROLE_USER")
def me():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    return user.serialize(), HTTP_200_OK


@auth.get('/token/refresh')
@jwt_required(refresh=True)
def refresh_users_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)
    return jsonify({
        'access': access
    }), HTTP_200_OK


# An endpoint that requires a valid fresh access token (non-expired and fresh only)
@auth.get("/token/valid")
@jwt_required()
def is_valid_token():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    return user.serialize(), HTTP_200_OK


