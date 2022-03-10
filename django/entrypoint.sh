#!/bin/bash

sleep 60

python3 /var/lib/django/BankAccount/manage.py makemigrations
python3 /var/lib/django/BankAccount/manage.py migrate
python3 /var/lib/django/BankAccount/manage.py collectstatic --noinput

supervisord -n -c /etc/supervisor/supervisord.conf
