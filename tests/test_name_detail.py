import pytest

from name.models import Name
from django.core.urlresolvers import reverse

# Mark all tests in this file as requiring database access.
pytestmark = pytest.mark.django_db


def test_person_itemprops(client):
    """Verify the correct item properties are included in
    the rendered page.

    A Person should have:
        - Name
        - URL
        - Birth Date
    """
    name = Name.objects.create(name='test person',
                               name_type=0, begin='2012-01-12')
    response = client.get(
        reverse('name_entry_detail', args=[name.name_id]))

    assert 'itemprop=\"name\"' in response.content
    assert 'itemprop=\'url\'' in response.content
    assert 'itemprop=\"birthDate\"' in response.content


def test_building_itemprops(client):
    """Verify the correct item properties are included in
    the rendered page.

    A Building should have:
        - Name
        - URL
        - Erected Date
    """
    name = Name.objects.create(name='test building',
                               name_type=4, begin='2000-01-12')
    response = client.get(
        reverse('name_entry_detail', args=[name.name_id]))

    assert 'itemprop=\"name\"' in response.content
    assert 'itemprop=\'url\'' in response.content
    assert 'itemprop=\"erectedDate\"' in response.content


def test_organization_itemprops(client):
    """Verify the correct item properties are included in
    the rendered page.

    A Organization should have:
        - Name
        - URL
        - Founding Date
    """
    name = Name.objects.create(name='test organization',
                               name_type=1, begin='2000-01-12')
    response = client.get(
        reverse('name_entry_detail', args=[name.name_id]))

    assert 'itemprop=\"name\"' in response.content
    assert 'itemprop=\'url\'' in response.content
    assert 'itemprop=\"foundingDate\"' in response.content


def test_event_itemprops(client):
    """Verify the correct item properties are included in
    the rendered page.

    A Event should have:
        - Name
        - URL
        - Starting Date
    """
    name = Name.objects.create(name='test event',
                               name_type=2, begin='2500-01-12')
    response = client.get(
        reverse('name_entry_detail', args=[name.name_id]))

    assert 'itemprop=\"name\"' in response.content
    assert 'itemprop=\'url\'' in response.content
    assert 'itemprop=\"startDate\"' in response.content
