from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)
from passlib.hash import pbkdf2_sha256 as sha256

parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)

cache_db = {}


def generate_hash(password):
    return sha256.hash(password)


def verify_hash(password, hash_t):
    return sha256.verify(password, hash_t)


class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        username = data['username']
        password = generate_hash(data['password'])
        cache_db[username] = password
        # access_token = create_access_token(identity=data['username'])
        return {
                   'message': 'User {} was created'.format(data['username'])
               }, 200


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        try:
            user_password = cache_db[data['username']]
        except KeyError:
            user_password = ""
        if not user_password:
            return {'message': 'User {} doesn\'t exist. Forbidden'.format(data['username'])}, 403
        elif verify_hash(data['password'], user_password):
            access_token = create_access_token(identity=data['username'])
            return {'message': 'Logged in as {}'.format(data['username']), 'access_token': access_token}, 200
        else:
            return {'message': 'Forbidden'}, 403

