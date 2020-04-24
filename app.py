from flask import Flask, redirect, request
import requests
from flask_restful import Api
import json
from urllib.parse import urlparse
import tempfile
import re
import random
from flask_jwt_extended import jwt_required, get_jti
import sqlite3
from flask_restful import Resource, reqparse
from user import resources

app = Flask(__name__)
api = Api(app)

connection = sqlite3.connect('url.db', check_same_thread=False)
cursor = connection.cursor()
# connection.execute('''CREATE TABLE URLS
#          (ID INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL,
#          URL  TEXT    NOT NULL);''')


parser_linker = reqparse.RequestParser()

parser_linker_post = reqparse.RequestParser()
parser_linker_post.add_argument('link', help='Something went wrong', required=True)
parser_linker_post.add_argument('X-Access-Token', type=str, location='headers', required=True)

# char = lambda x: [char for char in x]
words = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def base62encode(number):
    buf = []
    base = len(words)
    while number:
        number, remainder = divmod(number, base)
        buf.append(words[remainder - 1])
    buf.reverse()
    return ''.join(buf)


def base62decode(hashed):
    base = len(words)
    number = 0
    strlen = len(hashed)
    id_x = 0

    for x in hashed:
        power = (strlen - (id_x + 1))
        number += words.index(x) * (base ** power)
        id_x += 1
    return number


def VerifyJwt(token):
    r = requests.post("http://0.0.0.0:3000/token/verify", headers={"Authorization": "Bearer " + token + ""})
    response = json.loads((r.content).decode('utf-8'))
    response_status = r.status_code
    if response_status == 200 and response['code'] == 1:
        return True
    else:
        return False


class urllinker(Resource):

    def get(self, id):
        redirect_url = connection.execute('SELECT URL FROM URLS WHERE ID = ' + str(base62decode(id)) + ';')
        url = ""

        for x in redirect_url:
            url = x[0]
        print(url)
        return redirect(url, code=301)

    def put(self, id):
        data = parser_linker_post.parse_args()
        urlparsed = urlparse(data['link'])
        if VerifyJwt(data['X-Access-Token']):
            if (urlparsed.scheme == "http" or urlparsed.scheme == "https"):
                redirect_url = connection.execute('SELECT URL FROM URLS WHERE ID = ' + str(base62decode(id)) + ';')
                url = ""

                for x in redirect_url:
                    url = x[0]

                if len(url) != 0:
                    cursor.execute(
                        '''UPDATE URLS SET URL="''' + urlparsed.geturl() + '''" WHERE id = ''' + str(base62decode(id)) +
                        ''' ;''')
                    row_id = cursor.lastrowid
                    hash = base62encode(row_id)
                    print(hash)
                    return {'id': hash, "changes": "ok"}, 201
                else:
                    return "Not found", 404

            elif (urlparsed.scheme == "javascript" or urlparsed.scheme == "data"):
                return "", 302, {'Location': "https://i.imgflip.com/2w8wup.jpg"}

            else:
                return "", 400
        else:
            return {"msg": "The resource is forbidden"}, 403

    def delete(self, id):
        data = parser_linker_post.parse_args()
        if VerifyJwt(data['X-Access-Token']):
            connection.execute('DELETE FROM URLS WHERE id = ' + str(base62decode(id)) + ';')
            return "", 204
        else:
            return {"msg": "The resource is forbidden"}, 403


class urllinkerpost(Resource):
    def post(self):
        data = parser_linker_post.parse_args()
        if VerifyJwt(data['X-Access-Token']):
            redirect_url = urlparse(data['link'])
            print(redirect_url.scheme)
            if (redirect_url.scheme == "http" or redirect_url.scheme == "https"):

                cursor.execute('''INSERT INTO URLS (URL)
                            VALUES ( "''' + redirect_url.geturl() + '''" );''')
                row_id = cursor.lastrowid
                hash = base62encode(row_id)
                print(hash)
                return {'id': hash}, 201

            elif (redirect_url.scheme == "javascript" or redirect_url.scheme == "data"):
                return "", 302, {'Location': "https://i.imgflip.com/2w8wup.jpg"}

            else:
                return "", 400
        else:
            return {"msg": "The resource is forbidden"}, 403

    def delete(self):
        data = parser_linker_post.parse_args()
        if VerifyJwt(data['X-Access-Token']):
            connection.execute('TRUNCATE TABLE URLS;')
            return "", 204
        else:
            return {"msg": "The resource is forbidden"}, 403

    def get(self):
        try:
            redirect_url = connection.execute('SELECT URL FROM URLS;')
            url = []
            for x in redirect_url:
                url.append(x[0])
            return {"id": url, "status": 301}, 301
        except Exception as e:
            return {}, 404


api.add_resource(urllinker, '/<string:id>')
api.add_resource(urllinkerpost, '/')

if __name__ == '__main__':
    app.run(debug=True)
