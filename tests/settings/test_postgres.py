from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'name',
        'USER': os.getenv('DB_POSTGRES_USER', default='name'),
        'PASSWORD': os.getenv('DB_PASSWORD', default='name'),
        'HOST': os.getenv('DB_HOST', default='postgres'),
    }
}
