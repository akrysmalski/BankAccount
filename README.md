# Bank account project for recruitment process
REST API backend which allows to create users, accounts and make transfers between them
## Endpoints:
    /api/v1/
 - [GET] /users/ - list all users in the system
 - [GET] /users/<pk>/ - retreive concrete user
 - [DELETE] /users/<pk>/ - delete an user
 - [POST] /users/ - create an user
 - [PUT] /users/<pk>/ - update an user
 - [PATCH] /users/<pk>/ - partially update an user
 - [POST] /users/<pk>/change_password/ - change user's password 
 - [GET] /accounts/ - list all accounts in the system
 - [GET] /accounts/<pk>/ - retreive concrete account
 - [DELETE] /accounts/<pk>/ - delete an account
 - [POST] /accounts/ - create an account
 - [PUT] /accounts/<pk>/ - update an account
 - [PATCH] /accounts/<pk>/ - partially update an account
 - [GET] /accounts/<pk>/history/ - account's transactions history
 - [POST] /accounts/<pk>/transfer/ - make a transfer from account

## Deployement

### Install Docker
Follow this tutorials based on your OS to install Docker and Docker compose (compose version 2.0.1):
https://docs.docker.com/engine/install/
https://docs.docker.com/compose/install/

### Run installation script
You will be prompted for Django admin email and password and password for postgres
```sh
cd /path/to/BankAccount
sudo chmod +x install.sh
./install.sh
```
That's it, you can access the app (https://127.0.0.1)

## For development
If you want run Django development server only (without whole Docker staff):
```sh
cd /path/to/BankAccount/django
touch BankAccount/BankAccount/settings_dev.py
python -m venv env
source env/bin/activate
python -m pip install -r BankAccount/requirements.txt
python BankAccount/manage.py runserver
```
