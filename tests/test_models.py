import json
from datetime import datetime

import pytest
from django.utils import timezone
from mock import patch, Mock

from name.models import (
    Name,
    NameManager,
    Note,
    Variant,
    BaseTicketing,
    Location,
    Identifier_Type,
    Identifier)


class TestIdentifier_Type:
    def test_has_unicode_method(self):
        label = "Test Label"
        identifer = Identifier_Type(label=label)
        assert label == unicode(identifer)


class TestIdentifier:
    def test_has_unicode_method(self):
        value = "Test Value"
        identifer = Identifier(value=value)
        assert value == unicode(identifer)


class TestNote:
    def test_has_unicode_method(self):
        msg = "Test Note"
        note = Note(note=msg)
        assert msg == unicode(note)


class TestVariant:
    def test_has_unicode_method(self):
        variant_variant = "Test Variant"
        variant = Variant(variant=variant_variant)
        assert variant_variant == unicode(variant)


class TestBaseTicketing:
    def test_has_unicode_method(self):
        ticket_id = 1
        ticket = BaseTicketing(id=ticket_id)
        assert 'nm{:07d}'.format(ticket_id) == unicode(ticket)


class TestNameManager(object):

    @pytest.fixture
    def time_series_names(self):
        for _ in range(10):
            name = Name.objects.create(name="John Smith", name_type=Name.PERSONAL)  # noqa
            name.date_created = datetime(year=2014, month=10, day=11)
            name.save()

        for _ in range(10):
            name = Name.objects.create(name="John Smith", name_type=Name.PERSONAL)  # noqa

    @pytest.mark.django_db
    def test_created_stats(self, time_series_names):
        manager = NameManager()
        manager.model = Name

        stats = manager.created_stats()

        assert len(stats) == 2
        assert all(m['count'] == 10 for m in stats)
        assert all(timezone.is_aware(m['month']) for m in stats)

    @pytest.mark.django_db
    def test_modified_stats(self, time_series_names):
        manager = NameManager()
        manager.model = Name

        stats = manager.modified_stats()

        assert len(stats) == 1
        assert all(m['count'] == 20 for m in stats)
        assert all(timezone.is_aware(m['month']) for m in stats)


class TestName:
    @pytest.mark.django_db
    def test_saving_name_increments_base_ticketing_id(self):
        """Test that the BaseTicketing ID is properly incremented
        when a Name object is saved to the database.
        """
        # Create an initial Name so we can be confident that
        # a BaseTicketing Object will exist
        Name.objects.create(name="Test Name", name_type=Name.ORGANIZATION)
        first_id = BaseTicketing.objects.all().last().id
        Name.objects.create(name="Test Name", name_type=Name.ORGANIZATION)
        second_id = BaseTicketing.objects.all().last().id
        assert second_id == first_id + 1

    @pytest.mark.django_db
    def test_saving_name_creates_location(self):
        """Test that a Location is created when the Name object
        is a location (4) and does not have any associated Location
        objects.
        """
        lat, lng = 33.210241, -97.148857
        with patch('name.models.urlopen') as mock_urlopen:
            mock_urlopen.return_value = mock_response = Mock()
            mock_response.status_code = 200

            # The json payload from map.googleapis.com is expected to
            # look something like this.
            mock_response.read.return_value = json.dumps(
                {
                    'status': "OK",
                    'results': [{
                        'geometry': {
                            'location': {'lat': lat, 'lng': lng}
                        }
                    }]
                }
            )

            name = Name.objects.create(
                name="Test Location",
                name_type=Name.BUILDING)

            locations = (Location.objects.all()
                         .filter(belong_to_name=name))

            assert 1 == locations.count()
            # Assert the location matches the data from the json
            # payload.
            assert lng == float(locations.first().longitude)
            assert lat == float(locations.first().latitude)

    @pytest.mark.django_db
    def test_saving_name_does_not_create_location(self):
        """Test that a Location is not created when the API returns
        more than one resource.
        """
        lat, lng = 33.210241, -97.148857
        with patch('name.models.urlopen') as mock_urlopen:
            mock_urlopen.return_value = mock_response = Mock()
            mock_response.status_code = 200

            # The json payload from map.googleapis.com is expected to
            # look something like this.
            mock_response.read.return_value = json.dumps(
                {
                    'status': "OK",
                    'results': [
                        {
                            'geometry': {
                                'location': {'lat': lat, 'lng': lng}
                            }
                        },
                        {
                            'geometry': {
                                'location': {'lat': lat + 5, 'lng': lng + 5}
                            }
                        }
                    ]
                }
            )

            name = Name.objects.create(
                name="Test Location",
                name_type=Name.BUILDING)

            assert 0 == name.location_set.count()

    @pytest.mark.django_db
    def test_has_geocode(self):
        """Test that has_geocode returns True."""

        lat, lng = 33.210241, -97.148857
        name = Name.objects.create(name="Test Name", name_type=Name.PERSONAL)
        Location.objects.create(belong_to_name=name, longitude=lng,
                                latitude=lat)
        assert name.has_geocode()

    @pytest.mark.django_db
    def test_does_not_have_geocode(self):
        """Test that has_geocode returns False."""
        name = Name.objects.create(name="Test Name", name_type=Name.PERSONAL)
        assert not name.has_geocode()

    def test_has_unicode_method(self):
        name_id = "0001"
        name = Name(name_id=name_id)
        assert name_id == unicode(name)


class TestLocation:
    def test_has_unicode_method(self):
        lat_lng = 239
        location = Location(latitude=lat_lng, longitude=lat_lng)
        assert location.geo_point() == unicode(location)

    @pytest.fixture
    def location_fixture(self, db, scope="class"):
        """Class level fixture of multiple Location objects."""
        name = Name.objects.create(name="Event", name_type=Name.SOFTWARE)
        loc1 = Location.objects.create(
            status=0,
            latitude=33.210241,
            longitude=-97.148857,
            belong_to_name=name)

        loc2 = Location.objects.create(
            status=0,
            latitude=33.210241,
            longitude=-97.148857,
            belong_to_name=name)

        loc3 = Location.objects.create(
            status=0,
            latitude=33.210241,
            longitude=-97.148857,
            belong_to_name=name)

        # Only return the ids, because the tests will
        # need to instantiate a new object to get the correct
        # statuses.
        return loc1.id, loc2.id, loc3.id

    @pytest.mark.django_db
    def test_save_updates_current_location_on_create(self, location_fixture):
        """Test that the Location status is properly updated during
        when calling the create method.

        The expected outcome here is that the last Location created
        will be designated as the current Location.
        """
        loc1, loc2, loc3 = location_fixture

        location1 = Location.objects.get(id=loc1)
        location2 = Location.objects.get(id=loc2)
        location3 = Location.objects.get(id=loc3)

        # The active location should be the last one that was created
        assert location1.status == Location.FORMER
        assert location2.status == Location.FORMER
        assert location3.status == Location.CURRENT

    @pytest.mark.django_db
    def test_save_updates_current_location_on_save(self, location_fixture):
        """Test that the Location status is properly updated during
        when calling the save method.

        The expected outcome here is that a when a Location is saved,
        the 'saved' location automatically becomes the current Location.
        """
        loc1, loc2, loc3 = location_fixture

        location1 = Location.objects.get(id=loc1)

        # Saving this location should make it the Active location.
        location1.status = Location.CURRENT
        location1.save()

        # Refresh/Get the objects to get the updated statuses.
        location1 = Location.objects.get(id=loc1)
        location2 = Location.objects.get(id=loc2)
        location3 = Location.objects.get(id=loc3)

        assert location1.status == Location.CURRENT
        assert location2.status == Location.FORMER
        assert location3.status == Location.FORMER
