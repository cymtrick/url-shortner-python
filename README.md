## User Service (Microservice 1)
### Running user microservice
- Go to `user` folder
- Run in cmd, `FLASK_APP=run.py FLASK_DEBUG=1 flask run --port=3000`
- By definition above, this microservice run in port 3000, you could change it by defining any port you want in `--port=` arguement.
- Routes:
    - `http://localhost:{port}/users` : User registration REST point, with requests to be given as `{
	"username": "DarthVader",
	"password": "Anakin Skywalker"
}`
    - Eg Response: `{
    "message": "User DarthVader was created"
}`
    - `http://localhost:{port}/users/login` : User login REST point, with requests to be given as `{
	"username": "Neeraj",
	"password": "12345"
}`
    - Eg Response: `{
    "message": "Logged in as DarthVader",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODc2ODQ2ODcsIm5iZiI6MTU4NzY4NDY4NywianRpIjoiNjg3NjBiYTktM2Y1MC00N2NmLThjZDItNzJkOGRlMjQ4YTgxIiwiZXhwIjoxNTg3Njg1NTg3LCJpZGVudGl0eSI6IkRhcnRoVmFkZXIiLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.XkuEXjbGByIrfco6fcQy_i5ZWwpal6j3M1e_liuz35s"
}`


### URL SHORTNER

Language `python3.7 `

Run venv first

`source venv/bin/activate`

Install required libraries using pip

`pip3 install requirements.txt`

run the app

`python3 app.py`

#### post request for id

Need to make three or four requests like these. There is a bug in which GET dosen't for work for the first ID.

Request
````
curl --location --request POST 'http://0.0.0.0:5000/' \
--header 'Content-Type: application/json' \
--data-raw '{
                        "link":"https://example.com"
	
}'
````

Response

response 201

````json
{
    "id": id_from_response
}
````

#### Get request for id

Request

````
curl --location --request GET 'http://0.0.0.0:5000/:id_get' \
--header 'Content-Type: application/json' \
````

Response

`301 redirect to the site`

#### Put request for id
Request

````
curl --location --request PUT 'http://0.0.0.0:5000/:id_to_be_changed' \
--header 'Content-Type: application/json' \
--data-raw '{
                        "link":"https://example.com"
	
}'
````
Response

````json
{
    "id": id_from_response,
    "changes": "ok"
}
````

#### Delete request for id

Request

````
curl --location --request DELETE 'http://0.0.0.0:5000/:id_to_delete' \
--header 'Content-Type: application/json' \
--data-raw ''
````

Response

`Header 204 No content`