
## Notice

**This app is currently undergoing major refactoring. Use at your own risk.** 

# Django Name [![Build Status](https://travis-ci.org/unt-libraries/django-name.svg?branch=master)](https://travis-ci.org/unt-libraries/django-name) [![Docs Status](https://img.shields.io/badge/docs-latest-blue.svg)](https://django-name.readthedocs.org) 

The Name App is a tool originally developed for documenting names used by the UNT Libraries in its various digital library systems and collections. The app provides a consistent way of communicating the authorized version of a name and information about the name that is useful for reuse. The Name App generates a unique URL for each name that can be used to unambiguously refer to a person, organization, event or piece of software. In addition to an HTML page for each name there are a number of other formats available for each record including a MADS XML version and a simple JSON representation. A key feature of the UNT Name App is the ability to link to other vocabularies such as the Virtual International Authority File (VIAF), the Library of Congress Name Authority File, or Wikipedia.  
 
 ---
 
## License

See LICENSE.

## Acknowledgements

django-name was developed at the UNT Libraries.

Contributors:

- [Joey Liechty](https://github.com/yeahdef)
- [Damon Kelley](https://github.com/damonkelley)
- [Lauren Ko](https://github.com/ldko)
- [Mark Phillips](https://github.com/vphill)


## Developing

To take advantage of the dev environment that is already configured, you need to have Docker(>= 1.3) and Docker Compose installed.

Install [Docker](https://docs.docker.com/installation/)

Install Docker Compose
```sh
$ pip install docker-compose
```

Clone the repository.
```sh
$ git clone https://github.com/unt-libraries/django-name.git
$ cd django-name
```

Start the app and run the migrations.
```sh
# start the app
$ docker-compose up -d

# run the migrations
$ docker-compose run --rm web ./manage.py migrate

# optional: add a superuser in order to login to the admin interface
$ docker-compose run --rm web ./manage.py createsuperuser
```

The code is in a volume that is shared between your workstation and the web container, which means any edits you make on your workstation will also be reflected in the Docker container. No need to rebuild the container to pick up changes in the code.

However, if the requirements files change, it is important that you rebuild the web container for those packages to be installed. This is something that could happen when switching between feature branches, or when pulling updates from the remote.

```sh
# stop the app
$ docker-compose stop

# remove the web container
$ docker-compose rm web

# rebuild the web container
$ docker-compose build web

# start the app
$ docker-compose up -d
```

#### Running the Tests
To run the tests via Tox, use this command.
```sh
$ docker-compose run --rm web tox
```
The Tox configuration will test this app with Django 1.6 - 1.8.

To run the tests only with the development environment (i.e. with Django 1.7)
```sh
$ docker-compose run --rm web ./runtests.py
```
Note: This is the same command that Tox issues inside each test environment it has defined.

