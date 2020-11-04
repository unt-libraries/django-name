
============
Installation
============

Requirements
------------

- Django 1.11
- Postgres or MySQL
- Django Admin - ``django.contrib.admin``
- Humanize - ``django.contrib.humanize``

.. note:: Django Name is intended to be installed within a Django project. If you are unfamiliar with Django, check out the docs_.

.. _docs: https://docs.djangoproject.com/en/1.11/

Installation
------------

1. Install the package from PyPI. ::

    $ pip install django-name


2. Add ``name`` to your ``INSTALLED_APPS``. Be sure to add ``django.contrib.admin`` and ``django.contrib.humanize`` if they are not already present. ::

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.humanize',
        # ...
        'name',
    )

3. Configure the context processors. ::

    TEMPLATES = [
        {
            'BACKEND': '...',
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    # ...
                    'django.contrib.auth.context_processors.auth',
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

    from name import urls as name_urls

    urlpatterns = [
        # ...
        path('name/', include(name_urls))
    ]


5. Migrate the database. ::

   $ ./manage.py migrate name


6. **Optional**: Load the Identifier Type fixtures. See :ref:`loading-fixtures-ref`.

.. _loading-fixtures-ref:

Loading Fixtures
----------------

.. note:: This is an optional installation step.

The app comes with a fixture of predefined Indentifier Types. Issue one of the following commands below install them.

.. code-block:: sh

   $ ./manage.py loaddata --app name identifier_types
