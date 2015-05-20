import pytest

from django.core.urlresolvers import reverse

from name.feeds import NameAtomFeed
from name.models import Name, Location

pytestmark = pytest.mark.django_db


def test_feed_has_georss_namespace(rf):
    request = rf.get(reverse('name_feed'))
    feed = NameAtomFeed()
    response = feed(request)
    assert 'xmlns:georss' in response.content


def test_feed_response_is_application_xml(rf):
    request = rf.get(reverse('name_feed'))
    feed = NameAtomFeed()
    response = feed(request)
    assert response['Content-Type'] == 'application/xml'


def test_feed_item_has_location(rf):
    name = Name.objects.create(name="Test", name_type=0)

    Location.objects.create(
        status=0,
        latitude=33.210241,
        longitude=-97.148857,
        belong_to_name=name)

    request = rf.get(reverse('name_feed'))
    feed = NameAtomFeed()
    response = feed(request)

    assert response.status_code == 200
    assert name.location_set.current_location.geo_point() in response.content


def test_feed_item_without_location(rf):
    Name.objects.create(name="Test", name_type=0)

    request = rf.get(reverse('name_feed'))
    feed = NameAtomFeed()
    response = feed(request)

    assert response.status_code == 200
