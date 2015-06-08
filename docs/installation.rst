
============
Installation
============

Requirements
------------

- Django 1.6+
- Postgres or MySQL
- Django Admin

.. note:: Django Name is intended to be installed within a Django project. If you are unfamiliar with Django, check out the docs_.

.. _docs: https://docs.djangoproject.com/en/1.8/

Installation
------------

1. Install the package from PyPI. ::

    $ pip install django-name


2. Add ``name`` to your ``INSTALLED_APPS``. Be sure to add ``django.contrib.admin`` if it is not already present. ::

    INSTALLED_APPS = (
        'django.contrib.admin',
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


4. Include the URLs. ::

    urlpatterns = [
        # ...
        url(r'^name/', include('name.urls', namespace='name'))
    ]


5. Migrate/Sync the database.


Django 1.7+ Migrations
----------------------

1. Run the migrations. ::

   $ ./manage.py migrate name

.. note:: If using Django 1.6, see :ref:`django-16-migrations-ref`.

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


4. Load the Identifier Type fixtures. (`Optional`) ::

   $ ./manage.py loaddata identifier_types

.. note:: To opt out of migrations for Django 1.6, do not install south, and just run ``$ ./manage.py syncdb``

.. _loading-fixtures-ref:

Loading Fixtures
----------------

.. note:: This is an optional installation step.

The app comes with a fixture of predefined Indentifier Types. Issue one of the following commands below install them.

.. code-block:: sh

   # Django 1.7+ 
   $ ./manage.py loaddata --app name identifier_types

   # Django 1.6
   $ ./manage.py loaddata identifier_types

