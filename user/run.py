from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'xN82fUMzVhxAmYawNPztNfSoakojpm88QQIMzfsnp5-eoc_pwoim7wkoA6xANJa7wMl4lR1txHDBSV1zmxsrErpNDOhYky9MH7ADTmBl-c3l_GgsKb1pDo6j1wb2P-ffNVyIdrAkGwZ7ZAVXOShR3za068a-8oGVAw7QsVo_Gcc'
jwt = JWTManager(app)
api = Api(app)

import views, resources

api.add_resource(resources.UserRegistration, '/users')
api.add_resource(resources.UserLogin, '/users/login')
api.add_resource(resources.JwtVerify, '/token/verify')