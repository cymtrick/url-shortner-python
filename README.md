# Web Services and Cloud-Based Systems - Assignment 2 (Microservices)
## Group 16 (Neeraj, Prashanth, Vignesh)
Refer to the last section, on how to integrate the microservices using an api gateway to create a common entry point using Nginx Server. (Bonus implementation)
- Language `python3.7 `
- Run venv first
`source venv/bin/activate`
- Install required libraries using pip
`pip3 install -r requirements.txt`
## User Service (Microservice 1)
### Running user microservice
- Go to `user` folder
- Run in cmd, `FLASK_APP=run.py FLASK_DEBUG=1 flask run --port=3000`
- By definition above, this microservice runs in port `3000`, you could change it by defining any port you want in `--port` flag.
- Routes:
    - `http://localhost:{port}/users` : User registration REST point, with requests to be given as `{
	"username": "DarthVader",
	"password": "Anakin Skywalker"
}`
    - Eg Response: `{
    "message": "User DarthVader was created"
}` with status code `200`.
    - `http://localhost:{port}/users/login` : User login REST point, with requests to be given as `{
	"username": "Neeraj",
	"password": "12345"
}`
    - Eg Response: `{
    "message": "Logged in as DarthVader",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODc2ODQ2ODcsIm5iZiI6MTU4NzY4NDY4NywianRpIjoiNjg3NjBiYTktM2Y1MC00N2NmLThjZDItNzJkOGRlMjQ4YTgxIiwiZXhwIjoxNTg3Njg1NTg3LCJpZGVudGl0eSI6IkRhcnRoVmFkZXIiLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.XkuEXjbGByIrfco6fcQy_i5ZWwpal6j3M1e_liuz35s"
}` with status code `200` or `403` for forbidden message (invalid login).
- The `access_token` is fetched and given as header to get the url shortened data from the next microservice.


## URL Shortner (Microservice 2)
### Running the microservice


- In the main project folder:
- run the app `python3 app.py` or by defining the port `FLASK_APP=app.py FLASK_DEBUG=1 flask run --port=5000`
- By definition above, this microservice runs in port `5000`, you could change it by defining any port you want in `--port` flag.
- Do note, every time the server is refreshed, the db is truncated, so all the urls have to added again.
#### post request for id

Need to make three or four requests like these. There is a bug in which GET dosen't for work for the first ID.

Request
````
curl --location --request POST 'http://0.0.0.0:5000/' \
--header 'Content-Type: application/json' \
--header 'X-Access-Token: TOKEN' \
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
--header 'X-Access-Token: TOKEN' \
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
--header 'X-Access-Token: TOKEN' \
--data-raw '{"link": ""}'
````

Response

`Header 204 No content`

#### GET request for all ids

Request

````
curl --location --request GET 'http://0.0.0.0:5000/:id_to_delete' \
--header 'Content-Type: application/json' \
--header 'X-Access-Token: TOKEN' \
--data-raw '{"link": ""}'
````

Response

````
{
    "id": [
        "http://www.google.com",
        "http://www.google.com",
        "http://www.google.com"
    ],
    "status": 200
}

````

#### Delete request for all ids

Request

````
curl --location --request DELETE 'http://127.0.0.1:80/web/' \
--header 'Content-Type: application/json' \
--header 'X-Access-Token: Token' \
--data-raw '{"link":""}'
````

Response

status `204`

## Running an API gateway for common entry point
Implemented using nginx reverse proxy server.

- Download nginx server : https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-18-04-quickstart
- After downloading, go to nginx folder `/etc/nginx/conf.d`
- Open `default.conf`
- Add as shown below to the conf file:
`````
upstream users {
    server 127.0.0.1:3000;
}

upstream web {
    server 127.0.0.1:5000;
}

server {
    listen       80;
    server_name  localhost;

    #charset koi8-r;
    #access_log  /var/log/nginx/host.access.log  main;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }

    location /users/ {
	proxy_pass http://users/;
    }

    location /web/ {
	proxy_pass http://web/;
    }

    #error_page  404              /404.html;

    # redirect server error pages to the static page /50x.html
    #
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }

    # proxy the PHP scripts to Apache listening on 127.0.0.1:80
    #
    #location ~ \.php$ {
    #    proxy_pass   http://127.0.0.1;
    #}

    # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
    #
    #location ~ \.php$ {
    #    root           html;
    #    fastcgi_pass   127.0.0.1:9000;
    #    fastcgi_index  index.php;
    #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
    #    include        fastcgi_params;
    #}

    # deny access to .htaccess files, if Apache's document root
    # concurs with nginx's one
    #
    #location ~ /\.ht {
    #    deny  all;
    #}
}
`````

- upstream users and web are the two microservices running on 3000 and 5000 port.
- Link these upstream to `proxy_pass` configuration as shown above. one service with rest point `/users/`, and the url shortner service with restpoint starting as `/web/`.
- Restart nginx server `systemctl start nginx`
- Check the status: `systemctl status nginx`
    - Should show succesful run: 
````
      nginx.service - nginx - high performance web server
   Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: en
   Active: active (running) since Fri 2020-04-24 16:28:22 CEST; 7h ago
     Docs: http://nginx.org/en/docs/
  Process: 21038 ExecStop=/bin/kill -s TERM $MAINPID (code=exited, status=0/SUCC
  Process: 21552 ExecStart=/usr/sbin/nginx -c /etc/nginx/nginx.conf (code=exited
 Main PID: 21553 (nginx)
    Tasks: 2 (limit: 4915)
   CGroup: /system.slice/nginx.service
           ├─21553 nginx: master process /usr/sbin/nginx -c /etc/nginx/nginx.con
           └─21554 nginx: worker process

Apr 24 16:28:22 neeraj-Inspiron-7572 systemd[1]: Starting nginx - high performan
Apr 24 16:28:22 neeraj-Inspiron-7572 systemd[1]: Started nginx - high performanc
 ````

## Thank you!
### @Group 16