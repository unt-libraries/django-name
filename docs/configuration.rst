=============
Configuration
=============

The Name App provides a few configurable settings.

Settings
========

Feed
----

.. note:: All feed settings are optional.

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


.. warning:: If ``NAME_FEED_AUTHOR_NAME`` is set to ``None``, and ``NAME_FEED_AUTHOR_EMAIL`` and ``NAME_FEED_AUTHOR_LINK`` are not given alternative values, then the `<author/>` element will not be present in the feed and it will not be valid according the ATOM specification.
