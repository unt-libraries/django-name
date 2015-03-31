
## Notice

**This app is currently undergoing major refactoring. Use at your own risk.** 

# Django Name [![Build Status](https://travis-ci.org/unt-libraries/django-name.svg?branch=add-tests)](https://travis-ci.org/unt-libraries/django-name)

The Name App is a tool for originally developed for documenting names used by the UNT Libraries in its various digital library systems and collections. The app provides a consistent way of communicating the authorized version of a name and information about the name that is useful for reuse. The Name App generates a unique URL for each name that can be used to unambiguously refer to a person, organization, event or piece of software. In addition to an HTML page for each name there are a number of other formats available for each record including a MADS XML version and a simple JSON representation. A key feature of the UNT Name App is the ability to link to other vocabularies such as the Virtual International Authority File (VIAF), the Library of Congress Name Authority File, or Wikipedia.  
 
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

To take advantage of the dev environment that is already configured, you need to have [Docker](https://docs.docker.com/) and [Docker Compose](https://docs.docker.com/compose/install/) installed.

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
```

The code is in a volume that is shared between your workstation and the web container, which means any edits you make on your workstation will also be reflected in the Docker container. No need to rebuild the container.

#### Running the Tests
To run the tests via Tox, use this command.
```sh
$ docker-compose run --rm web tox
```
The Tox configuration will test this app with Django 1.6 - 1.8beta.

To run the tests only with development environment (i.e. with Django 1.7)
```sh
$ docker-compose run --rm web ./runtests.py
```
Note: This is the same command that Tox issues inside each test environment is has defined.

