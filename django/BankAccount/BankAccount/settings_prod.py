import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = os.environ['DJANGO_SECRET']


DEBUG = False


ALLOWED_HOSTS = ['localhost', '127.0.0.1']


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


X_FRAME_OPTIONS = 'DENY'


CSRF_COOKIE_SECURE = True


SECURE_CONTENT_TYPE_NOSNIFF = True


SECURE_BROWSER_XSS_FILTER = True


SESSION_COOKIE_SECURE = True


SECURE_SSL_REDIRECT = True


SECURE_HSTS_SECONDS = 60


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/django.log'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True
        }
    }
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bank_account',
        'USER': 'bank_account',
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': 'postgresql',
        'PORT': '5432'
    }
}


STATIC_ROOT = '/var/lib/django/static'


MEDIA_ROOT = '/var/lib/django/media'