=============
Configuration
=============

The Name App provides a few configurable settings.

Settings
========

.. _configuration-branding:

Branding
--------

``NAME_APP_TITLE``
..................

**Default**: ``"Django Name"``

This is displayed in the navbar and throughout the templates.


``NAME_ADMIN_EMAIL``
....................

**Default**: ``None``

When set, this will display on the about page as a point of contact for adding name records to the app.

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
