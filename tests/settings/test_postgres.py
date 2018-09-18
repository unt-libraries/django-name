from .base import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'name',
        'USER': os.getenv('DB_POSTGRES_USER', default='name'),  # noqa
        'PASSWORD': os.getenv('DB_PASSWORD', default='name'),  # noqa
        'HOST': os.getenv('DB_HOST', default='postgres'),  # noqa
    }
}
