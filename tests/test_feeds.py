import pytest

from django.core.urlresolvers import reverse

from name.models import Name, Location

pytestmark = pytest.mark.django_db


def test_feed_has_georss_namespace(client):
    response = client.get(reverse('name_feed'))
    assert 'xmlns:georss' in response.content


def test_feed_response_is_application_xml(client):
    response = client.get(reverse('name_feed'))
    assert response['Content-Type'] == 'application/xml'


def test_feed_item_has_location(client):
    name = Name.objects.create(name="Test", name_type=0)

    Location.objects.create(
        status=0,
        latitude=33.210241,
        longitude=-97.148857,
        belong_to_name=name)

    response = client.get(reverse('name_feed'))
    assert name.location_set.current_location.geo_point() in response.content
