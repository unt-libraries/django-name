import pytest
import random
from name import models


@pytest.fixture
def name_fixture(db, scope="module"):
    '''Single Name object of type Person'''
    return models.Name.objects.create(
        name='test person',
        name_type=0,
        begin='2012-01-12')


@pytest.fixture
def name_fixtures(db, scope="module"):
    '''5 Name objects, one for each type.'''
    models.Name.objects.create(name='test person',
                               name_type=0, begin='2012-01-12')
    models.Name.objects.create(name='test organization',
                               name_type=1, begin='2000-01-12')
    models.Name.objects.create(name='test event',
                               name_type=2, begin='2500-01-12')
    models.Name.objects.create(name='test building',
                               name_type=4, begin='2000-01-12')


@pytest.fixture
def twenty_name_fixtures(db, scope="session"):
    '''Twenty Name objects.

    The name type for each object is randomly determined.
    This fixture is good for testing search functionality, or
    any occasion where you need a large amount of Names and
    the type of those Names is arbitrary.
    '''
    for x in range(21):
        models.Name.objects.create(
            name="Name {0}".format(x),
            name_type=random.randint(0, 4),
            begin='2012-01-12')
    return models.Name.objects.all()


@pytest.fixture
def merged_name_fixtures(db, scope="module"):
    '''Fixture that is preconfigured for testing Name merging.'''
    name1 = models.Name.objects.create(name='test person 1', name_type=0)
    name2 = models.Name.objects.create(name='test person 2', name_type=0)
    name1.merged_with = name2
    name1.save()
    return (name1, name2)


@pytest.fixture
def status_name_fixtures(db, scope="module"):
    '''Fixture that is preconfigured for testing Name merging.'''
    for x in range(0, 5):
        models.Name.objects.create(name='test 1', name_type=x,
                                   record_status=0)
        models.Name.objects.create(name='test 2', name_type=x,
                                   record_status=1)
        models.Name.objects.create(name='test 3', name_type=x,
                                   record_status=2)


@pytest.fixture
def search_fixtures(db, scope='module'):
    '''Name fixtures for search.

    This fixture provide 20 name fixtures with, 4 of each name type.
    This fixture is good for testing search functionality, or
    any occasion where you need a large amount of Names.
    '''
    for x in range(1, 5):
        models.Name.objects.create(
            name="Personal {0}".format(x), name_type=0)
        models.Name.objects.create(
            name="Organization {0}".format(x), name_type=1)
        models.Name.objects.create(
            name="Event {0}".format(x), name_type=2)
        models.Name.objects.create(
            name="Software {0}".format(x), name_type=3)
        models.Name.objects.create(
            name="Building {0}".format(x), name_type=4)
    return models.Name.objects.all()
