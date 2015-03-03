import os
local_path = lambda path: os.path.join(os.path.dirname(__file__), path)


APP_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..'))

DEBUG = True

SECRET_KEY = 'not-so-secret-for-tests'

SITE_ID = 1

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.humanize',
    'debug_toolbar',
    'markdown_deux',
    'name',
    'tests']

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware')

ROOT_URLCONF = 'tests.urls'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',)

TEMPLATE_DIRS = (
    local_path('templates'),
)

VOCAB_DOMAIN = 'http://localhost/'

MAINTENANCE_MSG = None

MEDIA_URL = '/media/'

STATIC_URL = '/static/'

MEDIA_ROOT = local_path('media')
