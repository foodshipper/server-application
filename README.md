# server-application
Server written in Python for the Foodship Android App

# API Documentation
[Read More](ean/endpoints/Endpoints.md)

# Installation
* You need an installed PostgreSQL Database and a Webserver like nginx or apache.
```bash
sudo apt-get install python3-venv # Install system requirements
python3 -m venv . # Create virtual environment
source bin/activate # Switch to virtualenv
git clone https://github.com/foodshipper/server-application.git # Clone the repo
cd server-application
pip3 install -r requirements.txt # Install python modules
cp foodship-api.ini ../
```

* You have to adapt the database credentials in ```foodship-api.ini```
* You have to add a config file for your webserver, eg nginx:

```
server {
	listen 80;
	server_name $DOMAIN;

	root $PATH_TO_APP_DIR;

	access_log $PATH_TO_APP_DIR/logs/access.log;
    error_log $PATH_TO_APP_DIR/logs/error.log;  

	location / {
		proxy_set_header X-Forward-For $proxy_add_x_forwarded_for;
		proxy_set_header Host $http_host;
        proxy_redirect off;
		if (!-f $request_filename) {
			proxy_pass http://127.0.0.1:8080;
			break;
		}
	}
}
```

* Now you can start your circus daemon
```
circusd --daemon foodship-api.ini
```