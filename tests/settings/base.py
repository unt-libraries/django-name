import os


APP_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..'))

DEBUG = True

SECRET_KEY = 'not-so-secret-for-tests'

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.humanize',
    'name',
    'tests',
]


ROOT_URLCONF = 'tests.urls'

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]


# Minimal template settings for testing Django 1.8.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.request',
                'name.context_processors.name'
            ],
        },
    },
]

STATIC_URL = '/static/'

TIME_ZONE = 'UTC'

USE_TZ = True
