from .base import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'name',
        'USER': os.getenv('DB_MYSQL_USER', default='root'),  # noqa
        'PASSWORD': os.getenv('DB_PASSWORD', default='root'),  # noqa
        'HOST': os.getenv('DB_HOST', default='mariadb'),  # noqa
    }
}
