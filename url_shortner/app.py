from flask import Flask , redirect
from flask_restful import Api
from urllib.parse import urlparse
import tempfile
import re
import random
import sqlite3
from flask_restful import Resource, reqparse

app = Flask(__name__)
api = Api(app)

connection = sqlite3.connect('url.db',check_same_thread=False)
cursor = connection.cursor()
# connection.execute('''CREATE TABLE URLS
#          (ID INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL,
#          URL  TEXT    NOT NULL);''')


parser_linker = reqparse.RequestParser()

parser_linker_post = reqparse.RequestParser()
parser_linker_post.add_argument('link', help='Something went wrong', required=True)

# char = lambda x: [char for char in x]
words = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def base62encode(number):

    buf = []
    base = len(words)
    while number:
        number, remainder =  divmod(number,base)
        buf.append(words[remainder-1])
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


class urllinker(Resource):

    def get(self,id):
        redirect_url = connection.execute('SELECT URL FROM URLS WHERE ID = ' + str(base62decode(id)) + ';')
        url = ""

        for x in redirect_url:
            url = x[0]
        print(url)
        return redirect(url,code=301)


    def put(self,id):
        data = parser_linker_post.parse_args()
        urlparsed = urlparse(data['link'])
        if (urlparsed.scheme == "http" or urlparsed.scheme == "https"):
            redirect_url = connection.execute('SELECT URL FROM URLS WHERE ID = ' + str(base62decode(id)) + ';')
            url = ""

            for x in redirect_url:
                url = x[0]

            if len(url) != 0:
                cursor.execute('''UPDATE URLS SET URL="''' + urlparsed.geturl() +'''" WHERE id = ''' + str(base62decode(id)) +
                               ''' ;''')
                row_id = cursor.lastrowid
                hash = base62encode(row_id)
                print(hash)
                return {'id':hash,"changes":"ok"},201
            else:
                return "Not found", 404

        elif (urlparsed.scheme == "javascript" or urlparsed.scheme == "data"):
            return "",302,{'Location': "https://i.imgflip.com/2w8wup.jpg"}

        else :
            return "", 400

    def delete(self,id):
        connection.execute('DELETE FROM URLS WHERE id = '+ str(base62decode(id)) +';')
        return "",204



class urllinkerpost(Resource):
    def post(self):
        data = parser_linker_post.parse_args()
        redirect_url = urlparse(data['link'])
        print(redirect_url.scheme)
        if (redirect_url.scheme == "http" or redirect_url.scheme == "https"):

            cursor.execute('''INSERT INTO URLS (URL)
                        VALUES ( "'''+ redirect_url.geturl() +'''" );''')
            row_id = cursor.lastrowid
            hash = base62encode(row_id)
            print(hash)
            return {'id':hash},201

        elif (redirect_url.scheme == "javascript" or redirect_url.scheme == "data"):
            return "",302,{'Location': "https://i.imgflip.com/2w8wup.jpg"}

        else :
            return "", 400

    def delete(self,id):
        return "",204




api.add_resource(urllinker,'/<string:id>')
api.add_resource(urllinkerpost,'/')





if __name__ == '__main__':
    app.run(debug=True)



