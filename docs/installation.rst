
============
Installation
============

1. Install the package from Github ::

    $ pip install http://github.com/unt-libraries/django-name

.. note::
    This package is not yet available on PyPI.
    

2. Add it to your ``INSTALLED_APPS`` ::

    INSTALLED_APPS = (
        # ...
        'name',
    )

3. Configure ``TEMPLATE_CONTEXT_PROCESSORS`` ::

    from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

    TEMPLATE_CONTEXT_PROCESSORS += (
        'django.core.context_processors.request',
        'name.context_processors.name_types'
    )

- The ``request`` context processor is required by the Name app. The built-in templates require access to request parameters.

- The ``name_types`` processors enables the filter component of the search action.

4. Include the URLS ::

    urlpatterns = [
        ...
        url(r'^name/', include('name.urls', namespace='name'))
    ]
