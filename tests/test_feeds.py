import pytest

from django.core.urlresolvers import reverse

from name.feeds import NameAtomFeed
from name.models import Name

# Give all tests access to the database.
pytestmark = pytest.mark.django_db


def test_feed_has_georss_namespace(rf):
    """Check that the georss namespace is present in the response
    content.
    """
    request = rf.get(reverse('name:feed'))
    feed = NameAtomFeed()
    response = feed(request)
    assert b'xmlns:georss' in response.content


def test_feed_response_is_application_xml(rf):
    """Verify the Content-Type header is set to `application/xml`."""
    request = rf.get(reverse('name:feed'))
    feed = NameAtomFeed()
    response = feed(request)
    assert response['Content-Type'] == 'application/xml'


def test_feed_item_with_location(rf):
    """Verify that the response returns ok when objects with locations
    are present in the feed.
    """
    name = Name.objects.create(name="Test", name_type=Name.PERSONAL)
    name.location_set.create(latitude=33.210241, longitude=-97.148857)

    request = rf.get(reverse('name:feed'))
    feed = NameAtomFeed()
    response = feed(request)

    assert response.status_code == 200


def test_feed_with_item_without_location(rf):
    """Verify that the response returns ok when objects without
    locations are present in the feed.
    """
    Name.objects.create(name="Test", name_type=Name.PERSONAL)

    request = rf.get(reverse('name:feed'))
    feed = NameAtomFeed()
    response = feed(request)

    assert response.status_code == 200


def test_feed_item_without_location_has_georss_element(rf):
    """Verify that the <georss:point> element is present for the
    feed entry.
    """
    name = Name.objects.create(name="Test", name_type=Name.PERSONAL)
    name.location_set.create(latitude=33.210241, longitude=-97.148857)

    request = rf.get(reverse('name:feed'))
    feed = NameAtomFeed()
    response = feed(request)

    assert b'<georss:point>' in response.content
    assert name.location_set.current_location.geo_point() in response.content.decode()


def test_feed_item_without_location_does_not_have_georss_element(rf):
    """Verify that the <georss:point> element is not present for the
    feed entry.
    """
    Name.objects.create(name="Test", name_type=Name.PERSONAL)

    request = rf.get(reverse('name:feed'))
    feed = NameAtomFeed()
    response = feed(request)

    assert b'<georss:point>' not in response.content
