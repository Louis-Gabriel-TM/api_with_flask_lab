from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api

from blacklist import BLACKLIST
from resources.user import TokenRefresh, User, UserLogin, UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True  # To see Flask JWT errors
app.config['JWT_BLASKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_SECRET_KEY'] = 'A First Secret Key for JWT Tokens'
app.secret_key = 'Another Secret Key'

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)  # don't create /auth endpoint


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:  # better should read from a config file or a db
        return {'is_admin': True}

    return {'is_admin': False}

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['identity'] in BLACKLIST

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': "The token has expired.",
        'error': "token_expired"
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': "Signature verification failed.",
        'error': "invalid_token"
    })

@jwt.unauthorized_loader
def missing_token_callback():
    return jsonify({
        'description': "Request dos not contain an access token",
        'error': "authorization_required"
    }), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': "The token is not fresh.",
        'error': "fresh_token_required"
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': "The token has been revoked.",
        'error': "token_revoked"
    }), 401


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserRegister, '/register')
api.add_resource(TokenRefresh, '/refresh')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
