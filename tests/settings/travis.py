from .base import *

# Database settings for TravisCI
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'name_test',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
    }
}
