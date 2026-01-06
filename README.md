# Django Name [![Build Status](https://github.com/unt-libraries/django-name/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/unt-libraries/django-name/actions) [![Docs Status](https://img.shields.io/badge/docs-latest-blue.svg)](https://django-name.readthedocs.org) [![PyPI Version](https://img.shields.io/pypi/v/django-name.svg)](https://pypi.python.org/pypi/django-name)
Python Implementation of NACO Normalization Rules

The Name App is a tool originally developed for documenting names used by the UNT Libraries in its various digital library systems and collections. The app provides a consistent way of communicating the authorized version of a name and information about the name that is useful for reuse. The Name App generates a unique URL for each name that can be used to unambiguously refer to a person, organization, event, building or piece of software. In addition to an HTML page for each name there are a number of other formats available for each record including a MADS XML version and a simple JSON representation. A key feature of the UNT Name App is the ability to link to other vocabularies such as the Virtual International Authority File (VIAF), the Library of Congress Name Authority File, or Wikipedia.  
 
 ---

## Installation

For installation instructions, see the [Installation](http://django-name.readthedocs.org/en/latest/installation.html) page in the docs.
 
## License

See LICENSE.

## Acknowledgements

django-name was developed at the UNT Libraries.

Contributors:

- [Joey Liechty](https://github.com/yeahdef)
- [Damon Kelley](https://github.com/damonkelley)
- [Lauren Ko](https://github.com/ldko)
- [Mark Phillips](https://github.com/vphill)
- [Gio Gottardi](https://github.com/somexpert)
- [Madhulika Bayyavarapu](https://github.com/madhulika95b)
- [Gracie Flores-Hays](https://github.com/gracieflores)


## Requirements
- Docker(>= 1.3) 
- Docker Compose


## Development

Install [Docker](https://docs.docker.com)

Install Docker Compose
```sh
$ pip install docker-compose
```

Clone the repository.
```sh
$ git clone https://github.com/unt-libraries/django-name.git
$ cd django-name
```

Warm up the Mariadb database. This only needs to be done when the database container doesn't exist yet. This will take about a minute once the image has been pulled.
```sh
$ docker-compose up -d mariadb
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
At this point you should be able to access your local instance of the site by visiting `<dockerhost>:8000/name/`

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

#### Developing with Podman and Podman-Compose
[Install or Enable Podman](https://podman.io/getting-started/installation).

[Install Podman Compose](https://github.com/containers/podman-compose).
```sh
$ sudo dnf install podman-compose
```

You will follow the same steps as above, starting with `Clone the repository`. For all of the docker steps, you will have to replace the word `docker` with `podman`.

If you have SELinux, you may need to temporarily add `:Z` to the web volumes in the docker-compose.yml. It will look like `.:/app/:Z`. You may also need to use `sudo` for your podman-compose commands.

#### Running the Tests
To run the tests via Tox, use this command. If you are using podman-compose, swap the word `docker` with `podman` for the commands below.
```sh
$ docker-compose run --rm web tox
```