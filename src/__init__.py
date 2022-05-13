from datetime import timedelta

from flask_cors import CORS
from flask import Flask, jsonify, send_from_directory
import os, pymysql
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from src.models.Database import db
from src.resources import auth, burgers_resources, client_addresses_resources, clients_resources, \
    client_addresses_resources, \
    menus_resources, orders_resources, payements_resources, users_resources, complements_types_resources, \
    complements_resources, images_resources, products_resources, statistiques_resources


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY'),
            JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=15),
            JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=30),
            UPLOAD_FOLDER=os.environ.get('UPLOAD_FOLDER'),

            SWAGGER={
                'title': "Brasil Burger API",
                'uiversion': 3
            }
        )
    else:
        app.config.from_mapping(test_config)
    db.app = app
    CORS(app, resources={r"*": {"origins": "*"}})
    UPLOAD_FOLDERS = './static/images/'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDERS
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    db.init_app(app)
    Migrate(app, db, directory='./src/migrations')
    #db.drop_all()
    db.create_all()

    JWTManager(app)
    #RESSOURCES
    app.register_blueprint(auth.auth)
    app.register_blueprint(burgers_resources.burgers)
    app.register_blueprint(users_resources.users)
    app.register_blueprint(clients_resources.clients)
    app.register_blueprint(client_addresses_resources.addresses)
    app.register_blueprint(complements_types_resources.complements_types)
    app.register_blueprint(complements_resources.complements)
    app.register_blueprint(menus_resources.menus)
    app.register_blueprint(orders_resources.orders)
    app.register_blueprint(images_resources.images)
    app.register_blueprint(products_resources.products)
    app.register_blueprint(statistiques_resources.statistiques)
    # Swagger(app, config=swagger_config, template=template)





    @app.get('/<short_url>')
    # @swag_from('./docs/short_url.yaml')
    def redirect_to_url(short_url):
        return jsonify({'error': 'Not found'}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({'error': 'Not found'}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({'error': 'Something went wrong, we are working on it'}), HTTP_500_INTERNAL_SERVER_ERROR

    return app
