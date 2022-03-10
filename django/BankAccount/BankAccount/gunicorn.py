import socket


bind = '0.0.0.0:8000'

loglevel = 'info'

accesslog = '/var/log/django/access.log'

errorlog = '/var/log/django/error.log'

proc_name = 'BankAccount'

workers = 3

forwarded_allow_ips = socket.gethostbyname('nginx')
