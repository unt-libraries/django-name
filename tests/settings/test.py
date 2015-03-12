from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'TEST_NAME': 'name-test',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'db',
    }
}
