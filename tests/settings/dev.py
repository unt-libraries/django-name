from .base import *  # noqa

INTERNAL_IPS = (
    '172.17.42.1',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'name',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'mysql',
    }
}
