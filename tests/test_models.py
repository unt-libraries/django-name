import pytest
import json
from mock import patch, Mock
from name import models


class TestIdentifier_Type:
    def test_has_unicode_method(self):
        label = "Test Label"
        identifer = models.Identifier_Type(label=label)
        assert label == unicode(identifer)


class TestIdentifier:
    def test_has_unicode_method(self):
        value = "Test Value"
        identifer = models.Identifier(value=value)
        assert value == unicode(identifer)


class TestNote:
    def test_has_unicode_method(self):
        msg = "Test Note"
        note = models.Note(note=msg)
        assert msg == unicode(note)


class TestVariant:
    def test_has_unicode_method(self):
        variant_variant = "Test Variant"
        variant = models.Variant(variant=variant_variant)
        assert variant_variant == unicode(variant)


class TestBaseTicketing:
    def test_has_unicode_method(self):
        ticket_id = 1
        ticket = models.BaseTicketing(id=ticket_id)
        assert 'nm{:07d}'.format(ticket_id) == unicode(ticket)


class TestName:
    @pytest.mark.django_db
    def test_saving_name_increments_base_ticketing_id(self):
        """Test that the BaseTicketing ID is properly incremented
        when a Name object is saved to the database.
        """
        # Create an initial Name so we can be confident that
        # a BaseTicketing Object will exist
        models.Name.objects.create(name="Test Name", name_type=1)
        first_id = models.BaseTicketing.objects.all().last().id
        models.Name.objects.create(name="Test Name", name_type=1)
        second_id = models.BaseTicketing.objects.all().last().id
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

            name = models.Name.objects.create(
                name="Test Location",
                name_type=4)

            locations = (models.Location.objects.all()
                         .filter(belong_to_name=name))

            assert 1 == locations.count()
            # Assert the location matches the data from the json
            # payload.
            assert lng == float(locations.first().longitude)
            assert lat == float(locations.first().latitude)

    @pytest.mark.django_db
    def test_has_geocode(self):
        """Test that has_geocode returns True."""

        lat, lng = 33.210241, -97.148857
        name = models.Name.objects.create(name="Test Name", name_type=4)
        models.Location.objects.create(belong_to_name=name, longitude=lng,
                                       latitude=lat)
        assert name.has_geocode()

    @pytest.mark.django_db
    def test_does_not_have_geocode(self):
        """Test that has_geocode returns False."""
        name = models.Name.objects.create(name="Test Name", name_type=4)
        assert not name.has_geocode()

    def test_has_unicode_method(self):
        name_id = "0001"
        name = models.Name(name_id=name_id)
        assert name_id == unicode(name)


class TestLocation:
    def test_has_unicode_method(self):
        lat_lng = 239
        location = models.Location(latitude=lat_lng, longitude=lat_lng)
        assert location.geo_point() == unicode(location)

    @pytest.fixture
    def location_fixture(self, db, scope="class"):
        """Class level fixture of multiple Location objects."""
        name = models.Name.objects.create(name="Event", name_type=3)
        loc1 = models.Location.objects.create(
            status=0,
            latitude=33.210241,
            longitude=-97.148857,
            belong_to_name=name)

        loc2 = models.Location.objects.create(
            status=0,
            latitude=33.210241,
            longitude=-97.148857,
            belong_to_name=name)

        loc3 = models.Location.objects.create(
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

        location1 = models.Location.objects.get(id=loc1)
        location2 = models.Location.objects.get(id=loc2)
        location3 = models.Location.objects.get(id=loc3)

        # The active location should be the last one that was created
        assert location1.status == models.Name.RECORD_STATUS_CHOICES[1][0]
        assert location2.status == models.Name.RECORD_STATUS_CHOICES[1][0]
        assert location3.status == models.Name.RECORD_STATUS_CHOICES[0][0]

    @pytest.mark.django_db
    def test_save_updates_current_location_on_save(self, location_fixture):
        """Test that the Location status is properly updated during
        when calling the save method.

        The expected outcome here is that a when a Location is saved,
        the 'saved' location automatically becomes the current Location.
        """
        loc1, loc2, loc3 = location_fixture

        location1 = models.Location.objects.get(id=loc1)

        # Saving this location should make it the Active location.
        location1.status = 0
        location1.save()

        # Refresh/Get the objects to get the updated statuses.
        location1 = models.Location.objects.get(id=loc1)
        location2 = models.Location.objects.get(id=loc2)
        location3 = models.Location.objects.get(id=loc3)

        assert location1.status == models.Name.RECORD_STATUS_CHOICES[0][0]
        assert location2.status == models.Name.RECORD_STATUS_CHOICES[1][0]
        assert location3.status == models.Name.RECORD_STATUS_CHOICES[1][0]
