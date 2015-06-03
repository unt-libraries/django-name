from .base import *

SOUTH_TESTS_MIGRATE = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'name',
        'USER': os.getenv('DB_MYSQL_USER', default="root"),
        'PASSWORD': os.getenv('DB_PASSWORD', default="root"),
        'HOST': os.getenv('DB_HOST', default='mysql'),
    }
}
