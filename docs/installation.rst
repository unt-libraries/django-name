
============
Installation
============

Requirements
------------

- Django >= 1.6
- Postgres or MySQL
- Django Admin


Installation
------------

1. Install the package from Github ::

    $ pip install http://github.com/unt-libraries/django-name

.. note::
    This package is not yet available on PyPI.
    

2. Add it to your ``INSTALLED_APPS`` ::

    INSTALLED_APPS = (
        # ...
        'name',
    )

3. Configure the context processors. 

- For Django 1.6 and 1.7 ::

    from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

    TEMPLATE_CONTEXT_PROCESSORS += (
        'django.core.context_processors.request',
        'name.context_processors.name'
    )

- For Django 1.8+ ::

    TEMPLATES = [
        {
            'BACKEND': '...',
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.request',
                    'name.context_processors.name'
                ],
                # ...
            },
        },
    ]
    

.. note:: The ``request`` context processor is required by the Name app. The built-in templates require access to request parameters.
    The ``name`` processor enables the filter component of the search action as well as some optional branding (see :ref:`configuration-branding`).


4. Include the URLS ::

    urlpatterns = [
        ...
        url(r'^name/', include('name.urls', namespace='name'))
    ]


5. Migrate/Sync the database.


Django 1.7+ Migrations
----------------------

1. Run the migrations ::

   $ ./manage.py migrate name

.. note:: If using Django 1.6, see :ref:`django-16-migrations-ref`.


2. Load the Identifier Type fixtures (`Optional`) ::

   $ ./manage.py loaddata --app name identifier_types


.. _django-16-migrations-ref:

Django 1.6 Migrations
---------------------

Django Name includes migrations that are compatible with South >= 1.0. Skip to step 3 if South is already installed. 

1. Install South. ::

    INSTALLED_APPS = [
        # ...
        south
    ]

2. Sync the database. ::

   $ ./manage.py syncdb

   

3. Run the migrations. ::

   $ ./manage.py migrate name


4. Load the Identifier Type fixtures (`Optional`) ::

   ./manage.py loaddata identifier_types

.. note:: To opt out of migrations for Django 1.6, do not install south, and just run ``$ ./manage.py syncdb``
