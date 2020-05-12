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
