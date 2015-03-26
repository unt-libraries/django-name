import pytest

from name.models import Name
from django.core.urlresolvers import reverse


@pytest.fixture
def name_fixtures(db, scope="module"):
    Name.objects.create(name='person', name_type=0, begin='2012-01-12')
    Name.objects.create(name='organization', name_type=1, begin='2000-01-12')
    Name.objects.create(name='event', name_type=2, begin='2500-01-12')
    Name.objects.create(name='building', name_type=4, begin='2000-01-12')


@pytest.mark.django_db
class TestNameDetailCase:
    """
    This class is intended to check that the intended html properties
    are showing correctly
    """
    def test_person_itemprops(self, client):
        name = Name.objects.create(name='test person',
                                   name_type=0, begin='2012-01-12')
        response = client.get(
            reverse('name_entry_detail', args=[name.name_id]))

        assert 'itemprop=\"name\"' in response.content
        assert 'itemprop=\'url\'' in response.content
        assert 'itemprop=\"birthDate\"' in response.content

    def test_building_itemprops(self, client):
        name = Name.objects.create(name='test building',
                                   name_type=4, begin='2000-01-12')
        response = client.get(
            reverse('name_entry_detail', args=[name.name_id]))

        assert 'itemprop=\"name\"' in response.content
        assert 'itemprop=\'url\'' in response.content
        assert 'itemprop=\"erectedDate\"' in response.content

    def test_organization_itemprops(self, client):
        name = Name.objects.create(name='test organization',
                                   name_type=1, begin='2000-01-12')
        response = client.get(
            reverse('name_entry_detail', args=[name.name_id]))

        assert 'itemprop=\"name\"' in response.content
        assert 'itemprop=\'url\'' in response.content
        assert 'itemprop=\"foundingDate\"' in response.content

    def test_event_itemprops(self, client):
        name = Name.objects.create(name='test event',
                                   name_type=2, begin='2500-01-12')
        response = client.get(
            reverse('name_entry_detail', args=[name.name_id]))

        assert 'itemprop=\"name\"' in response.content
        assert 'itemprop=\'url\'' in response.content
        assert 'itemprop=\"startDate\"' in response.content
