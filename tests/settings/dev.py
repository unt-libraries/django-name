from .base import *  # noqa


ALLOWED_HOSTS = INTERNAL_IPS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
]

# Required for viewing the debug toolbar in docker, since the IP address is unknown.
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda x: True,
}

INSTALLED_APPS += ['debug_toolbar']  # noqa

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'name',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'mysql',
    }
}
