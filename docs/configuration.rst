=============
Configuration
=============

The Name App provides a few configurable settings.

Settings
========

Branding
--------

To add a custom title and contact information add the following to your ``TEMPLATE_CONTEXT_PROCESSORS``::

    TEMPLATE_CONTEXT_PROCESSORS += (
        # ...
        'name.context_processors.branding'
    )

or for Django 1.8+ ::

    TEMPLATES = [
        # ...
        'OPTIONS': {
            'context_processors': [
                # ...
                'name.context_processors.branding'
            ]
        # ...
        ]
    ]

Adding this context processor enables the ``NAME_APP_TITLE`` and ``NAME_ADMIN_EMAIL`` settings.

``NAME_APP_TITLE``
..................

**Default**: ``"Django Name"``

This is displayed in the navbar and throughout the templates.


``NAME_ADMIN_EMAIL``
....................

**Default**: ``None``

When set, this will display on the about page as a point of contact for adding a name record to the app.

Feed
----

.. note:: All feed settings are optional. 

    For the feed to be valid according to the Atom specification, an ``<author/>`` element containing a ``<name/>`` element is required.

``NAME_FEED_AUTHOR_NAME``
.........................

**Default**: ``"Django Name"``

The author's name for the Name feed.


``NAME_FEED_AUTHOR_EMAIL``
..........................

**Default**: ``None``

The author's email for the Name feed.


``NAME_FEED_AUTHOR_LINK``
.........................

**Default**: ``None``

The author's URI for the Name feed.
