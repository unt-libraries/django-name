
===========
Development
===========

Development Environment
=======================

To take advantage of the dev environment that is already configured, you need to have Docker(>= 1.3) and Docker Compose installed.

Install Docker_

.. _Docker: https://docs.docker.com/installation/

Install Docker Compose.

.. code-block:: sh

    $ pip install docker-compose

Clone the repository. 

.. code-block:: sh

    $ git clone https://github.com/unt-libraries/django-name.git
    $ cd django-name

Start the app and run the migrations.

.. code-block:: sh

    # start the app
    $ docker-compose up -d

    # run the migrations
    $ docker-compose run --rm web ./manage.py migrate

    # optional: add a superuser in order to login to the admin interface
    $ docker-compose run --rm web ./manage.py createsuperuser

The code is in a volume that is shared between your workstation and the web container, which means any edits you make on your workstation will also be reflected in the Docker container. No need to rebuild the container to pick up changes in the code.

However, if the requirements files change, it is important that you rebuild the web container for those packages to be installed. This is something that could happen when switching between feature branches, or when pulling updates from the remote.

.. code-block:: sh

    # stop the app
    $ docker-compose stop

    # remove the web container
    $ docker-compose rm web

    # rebuild the web container
    $ docker-compose build web

    # start the app
    $ docker-compose up -d


Running the Tests
=================

To run the tests via Tox, use this command.

.. code-block:: sh

    $ docker-compose run --rm web tox

The Tox configuration will test this app with Django 1.6 - 1.8.

To run the tests only with the development environment (i.e. with Django 1.7).

.. code-block:: sh

    $ docker-compose run --rm web ./runtests.py

.. note::
    This is the same command that Tox issues inside each test environment it has defined.
