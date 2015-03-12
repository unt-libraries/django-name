# Test configuration for quick execution.
#
# This settings file will not work for tests against
# Django 1.6, as it does not support Auto incrementing primary
# keys in way required by django-name.
from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
