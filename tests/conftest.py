import pytest
import random
from name import models


@pytest.fixture
def name_fixture(db, scope="module"):
    return models.Name.objects.create(
        name='test person',
        name_type=0,
        begin='2012-01-12')


@pytest.fixture
def name_fixtures(db, scope="module"):
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
    for x in range(21):
        models.Name.objects.create(
            name="Name {}".format(x),
            name_type=random.randint(0, 4),
            begin='2012-01-12')
    return models.Name.objects.all()


@pytest.fixture
def merged_name_fixtures(db, scope="module"):
    name1 = models.Name.objects.create(name='test person 1', name_type=0)
    name2 = models.Name.objects.create(name='test person 2', name_type=0)
    name1.merged_with = name2
    name1.save()
    return (name1, name2)


@pytest.fixture
def search_fixtures(db, scope='module'):
    for x in range(1, 5):
        models.Name.objects.create(
            name="Personal {}".format(x), name_type=0)
        models.Name.objects.create(
            name="Organization {}".format(x), name_type=1)
        models.Name.objects.create(
            name="Event {}".format(x), name_type=2)
        models.Name.objects.create(
            name="Software {}".format(x), name_type=3)
        models.Name.objects.create(
            name="Building {}".format(x), name_type=4)
    return models.Name.objects.all()
