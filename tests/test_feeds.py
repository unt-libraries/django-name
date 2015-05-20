import pytest

from django.core.urlresolvers import reverse

from name.feeds import NameAtomFeed
from name.models import Name

# Give all tests access to the database.
pytestmark = pytest.mark.django_db


def test_feed_has_georss_namespace(rf):
    """Check that the georss namespace is present in the reponse
    content.
    """
    request = rf.get(reverse('name_feed'))
    feed = NameAtomFeed()
    response = feed(request)
    assert 'xmlns:georss' in response.content


def test_feed_response_is_application_xml(rf):
    """Verify the Content-Type header is set to `application/xml`."""
    request = rf.get(reverse('name_feed'))
    feed = NameAtomFeed()
    response = feed(request)
    assert response['Content-Type'] == 'application/xml'


def test_feed_item_with_location(rf):
    """Verify that the response is properly returned and that the
    object's geo point is present in the feed.
    """
    name = Name.objects.create(name="Test", name_type=0)
    name.location_set.create(latitude=33.210241, longitude=-97.148857)

    request = rf.get(reverse('name_feed'))
    feed = NameAtomFeed()
    response = feed(request)

    assert response.status_code == 200


def test_feed_with_item_without_location(rf):
    """Checks that an exception is not thrown if the feed includes
    an object that does not have a current location.
    """
    Name.objects.create(name="Test", name_type=0)

    request = rf.get(reverse('name_feed'))
    feed = NameAtomFeed()
    response = feed(request)

    assert response.status_code == 200


def test_feed_item_without_location_has_georss_element(rf):
    """Verify that the <georss:point> element is present for the
    feed entry.
    """
    name = Name.objects.create(name="Test", name_type=0)
    name.location_set.create(latitude=33.210241, longitude=-97.148857)

    request = rf.get(reverse('name_feed'))
    feed = NameAtomFeed()
    response = feed(request)

    assert '<georss:point>' in response.content
    assert name.location_set.current_location.geo_point() in response.content


def test_feed_item_without_location_does_not_have_georss_element(rf):
    """Verify that the <georss:point> element is not present for the
    feed entry.
    """
    Name.objects.create(name="Test", name_type=0)

    request = rf.get(reverse('name_feed'))
    feed = NameAtomFeed()
    response = feed(request)

    assert '<georss:point>' not in response.content
