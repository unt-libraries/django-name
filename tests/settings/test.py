from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'name_test',
        'USER': os.getenv('DB_USER', default="root"),
        'PASSWORD': os.getenv('DB_PASSWORD', default="root"),
        'HOST': os.getenv('DB_HOST', default='db'),
    }
}
