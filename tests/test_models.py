import pytest
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
        # Create an initial Name so we can be confident that
        # a BaseTicketing Object will exist
        models.Name.objects.create(name="Test Name", name_type=1)
        first_id = models.BaseTicketing.objects.all().last().id
        models.Name.objects.create(name="Test Name", name_type=1)
        second_id = models.BaseTicketing.objects.all().last().id
        assert second_id == first_id + 1

    # TODO: This is an unreliable test because is relies on
    # the Google Maps API to return a single result. If second result
    # is added for the name it will fail. Fixit.
    @pytest.mark.django_db
    def test_saving_name_creates_location(self):
        name = models.Name.objects.create(name="University of North Texas",
                                          name_type=4)
        assert 0 < (models.Location.objects.all()
                    .filter(belong_to_name=name).count())

    @pytest.mark.django_db
    def test_has_geocode(self):
        lat = 33.210241
        lng = -97.148857
        name = models.Name.objects.create(name="Test Name", name_type=4)
        models.Location.objects.create(belong_to_name=name, longitude=lng,
                                       latitude=lat)
        assert name.has_geocode()

    @pytest.mark.django_db
    def test_does_not_have_geocode(self):
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

    @pytest.mark.xfail
    def test_save(self):
        pass
