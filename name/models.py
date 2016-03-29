import json
from datetime import datetime
from itertools import groupby

import markdown2
from django.core.urlresolvers import reverse
from django.db import models, transaction
from django.utils import timezone
from django.utils.six.moves.urllib.parse import quote
from django.utils.six.moves.urllib.request import urlopen
from pynaco.naco import normalizeSimplified

from .validators import validate_merged_with


class Identifier_Type(models.Model):
    """Custom Identifier Type.

    Used in conjunction with the Identifier model.
    """
    label = models.CharField(
        max_length=255,
        help_text='What kind of data is this? Personal website? Twitter?')

    icon_path = models.CharField(
        max_length=255,
        blank=True,
        help_text='Path to icon image?')

    homepage = models.URLField(
        blank=True,
        help_text='Homepage of label. Twitter.com, Facebook.com, etc')

    class Meta:
        ordering = ['label']
        verbose_name = 'Identifier Type'

    def __unicode__(self):
        return self.label


class Identifier(models.Model):
    """An Identifier for a Name models instance. Most commonly
    represented as a permalink.

    This is used in conjunction with the Identifier Type model to
    specify the type of Identifier the instance represents. An example
    instance would have an Identifier Type of `Twitter` and the value
    field would have the permalink to the Name's Twitter profile page.
    """
    type = models.ForeignKey(
        'Identifier_Type',
        help_text="Catagorize this record's identifiers here")

    belong_to_name = models.ForeignKey('Name')
    value = models.CharField(max_length=500)
    visible = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'type']

    def __unicode__(self):
        return self.value


class NoteManager(models.Manager):
    """Custom Model Manager for the Note model."""
    use_for_related_fields = True

    def public_notes(self):
        return self.get_queryset().exclude(note_type=self.model.NONPUBLIC)


class Note(models.Model):
    """A note regarding the related Name model instance."""
    BIOGRAPHICAL_HISTORICAL = 0
    DELETION_INFORMATION = 1
    NONPUBLIC = 2
    SOURCE = 3
    OTHER = 4

    NOTE_TYPE_CHOICES = (
        (BIOGRAPHICAL_HISTORICAL, 'Biographical/Historical'),
        (DELETION_INFORMATION, 'Deletion Information'),
        (NONPUBLIC, 'Nonpublic'),
        (SOURCE, 'Source'),
        (OTHER, 'Other')
    )

    note = models.TextField(help_text='Enter notes about this record here')
    note_type = models.IntegerField(choices=NOTE_TYPE_CHOICES)
    belong_to_name = models.ForeignKey('Name')

    objects = NoteManager()

    def get_note_type_label(self):
        """Returns the label associated with an instance's
        note_type.
        """
        id, note_type = self.NOTE_TYPE_CHOICES[self.note_type]
        return note_type

    def __unicode__(self):
        return self.note


class Variant(models.Model):
    """Defines an alternative form that a Name may be displayed."""
    ACRONYM = 0
    ABBREVIATION = 1
    TRANSLATION = 2
    EXPANSION = 3
    OTHER = 4

    VARIANT_TYPE_CHOICES = (
        (ACRONYM, 'Acronym'),
        (ABBREVIATION, 'Abbreviation'),
        (TRANSLATION, 'Translation'),
        (EXPANSION, 'Expansion'),
        (OTHER, 'Other')
    )

    belong_to_name = models.ForeignKey('Name')
    variant_type = models.IntegerField(
        choices=VARIANT_TYPE_CHOICES,
        help_text='Choose variant type.')

    variant = models.CharField(
        max_length=255,
        help_text='Fill in the other name variants, if any.')

    normalized_variant = models.CharField(
        max_length=255,
        editable=False,
        help_text='NACO normalized variant text')

    def get_variant_type_label(self):
        """Returns the label associated with an instance's
        variant_type.
        """
        id, variant_type = self.VARIANT_TYPE_CHOICES[self.variant_type]
        return variant_type

    def save(self):
        self.normalized_variant = normalizeSimplified(self.variant)
        super(Variant, self).save()

    def __unicode__(self):
        return self.variant


class TicketingManager(models.Manager):
    """Custom manager for the BaseTicketing model."""

    def create(self, *args, **kwargs):
        """Override the create method.

        Create or get the single object. If one already exists,
        delete it and create a new one so we auto-increment the id.
        """
        obj, created = self.get_or_create(stub=self.model.STUB_DEFAULT)
        if not created:
            with transaction.atomic():
                obj.delete()
                obj = self.create(stub=self.model.STUB_DEFAULT)
        return obj


class BaseTicketing(models.Model):
    """Creates a custom app-level identifier.

    This leverages the autoincrement primary key field to
    create custom unique identifier. An example identifier
    would be `nm0000001`.
    """
    # Explicitly set the id of the model, even though it is the same
    # as the one Django gives it.
    id = models.AutoField(null=False, primary_key=True)

    # This is just the smallest placeholder we can create that we can
    # replace into to generate a new id.
    STUB_DEFAULT = True
    stub = models.BooleanField(null=False, default=STUB_DEFAULT, unique=True)

    # Override the default manager
    objects = TicketingManager()

    @property
    def ticket(self):
        """Alias for id"""
        return self.id

    def __unicode__(self):
        return u'nm{ticket:07d}'.format(ticket=self.ticket)


class NameManager(models.Manager):
    """Custom Manager for the Name model.

    Provides additional methods that are useful in calculating
    statistics on Name model instances.
    """

    def visible(self):
        """Retrieves all Name objects that have an Active record status
        and are not merged with any other Name objects.
        """
        return self.get_queryset().filter(
            record_status=self.model.ACTIVE, merged_with=None)

    def active_type_counts(self):
        """Calculates counts of Name objects by Name Type.

        Statistics are based off of the queryset returned by visible.
        The total number is calculated using the count method. All
        additional figures are calculated using Python to reduce the number
        of queries.
        """
        names = self.visible()
        return {
            'total': names.count(),
            'personal': len(filter(lambda n: n.is_personal(), names)),
            'organization': len(filter(lambda n: n.is_organization(), names)),
            'event': len(filter(lambda n: n.is_event(), names)),
            'software': len(filter(lambda n: n.is_software(), names)),
            'building': len(filter(lambda n: n.is_building(), names))
        }

    def _counts_per_month(self, date_column):
        """Calculates the number of Names by month according to the
        date_column passed in.

        This will return a ValueQuerySet where each element is in the form
        of
            {
               count: <Number of Names for the month>,
               month: <Datetime object for first day of the given month>
            }
        """
        def grouper(name):
            return (getattr(name, date_column).year,
                    getattr(name, date_column).month)

        def convert_key(year, month):
            datetime_obj = datetime(year=year, month=month, day=1)
            tzinfo = timezone.get_current_timezone()
            return timezone.make_aware(datetime_obj, tzinfo)

        results = self.all().order_by(date_column)

        return [
            dict(month=convert_key(*key), count=len(list(value)))
            for key, value in groupby(results, grouper)
        ]

    def created_stats(self):
        """Returns a list of the number of Names created per
        month.
        """
        return self._counts_per_month('date_created')

    def modified_stats(self):
        """Returns a list of the number of Names modified per
        month.
        """
        return self._counts_per_month('last_modified')


class Name(models.Model):
    """The authorized version of a name that is used to unambiguously
    refer to a person, organization, event, building or piece of
    software.
    """
    ACTIVE = 0
    DELETED = 1
    SUPPRESSED = 2

    RECORD_STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (DELETED, 'Deleted'),
        (SUPPRESSED, 'Suppressed')
    )

    PERSONAL = 0
    ORGANIZATION = 1
    EVENT = 2
    SOFTWARE = 3
    BUILDING = 4

    NAME_TYPE_CHOICES = (
        (PERSONAL, 'Personal'),
        (ORGANIZATION, 'Organization'),
        (EVENT, 'Event'),
        (SOFTWARE, 'Software'),
        (BUILDING, 'Building')
    )

    DATE_DISPLAY_LABELS = {
        PERSONAL: {
            'type': 'Personal',
            'begin': 'Date of Birth',
            'end': 'Date of Death'
        },
        ORGANIZATION: {
            'type': 'Organization',
            'begin': 'Founded Date',
            'end': 'Defunct'
        },
        EVENT: {
            'type': 'Event',
            'begin': 'Begin Date',
            'end': 'End Date'
        },
        SOFTWARE: {
            'type': 'Software',
            'begin': 'Begin Date',
            'end': 'End Date'
        },
        BUILDING: {
            'type': 'Building',
            'begin': 'Erected Date',
            'end': 'Demolished Date',
        },
        None: {
            'type': None,
            'begin': 'Born/Founded Date',
            'end': 'Died/Defunct Date'
        }
    }

    NAME_TYPE_SCHEMAS = {
        PERSONAL: 'http://schema.org/Person',
        ORGANIZATION: 'http://schema.org/Organization',
        BUILDING: 'http://schema.org/Place'
    }

    name = models.CharField(
        max_length=255,
        help_text='Please use the general reverse order: LAST, FIRST')

    normalized_name = models.CharField(
        max_length=255,
        editable=False,
        help_text='NACO normalized form of the name')

    name_type = models.IntegerField(choices=NAME_TYPE_CHOICES)

    # Date, month or year of birth or incorporation of the name
    begin = models.CharField(
        max_length=25,
        blank=True,
        help_text='Conforms to EDTF format YYYY-MM-DD')

    # Date, month of year of death or un-incorporation of the name
    end = models.CharField(
        max_length=25,
        blank=True,
        help_text='Conforms to EDTF format YYYY-MM-DD')

    disambiguation = models.CharField(
        max_length=255,
        blank=True,
        help_text='Clarify to whom or what this record pertains.')

    biography = models.TextField(
        blank=True,
        help_text='Compatible with MARKDOWN')

    record_status = models.IntegerField(
        default=ACTIVE,
        choices=RECORD_STATUS_CHOICES)

    merged_with = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='merged_with_name')

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    name_id = models.CharField(max_length=10, unique=True, editable=False)

    objects = NameManager()

    def get_absolute_url(self):
        """Get the absolute url to the Name detail page."""
        return reverse('name:detail', args=[self.name_id])

    def get_schema_url(self):
        """Get the appropriate schema url based on the name type."""
        return self.NAME_TYPE_SCHEMAS.get(self.name_type, None)

    def get_name_type_label(self):
        """Get the string form of the Name's name type."""
        id, name_type = self.NAME_TYPE_CHOICES[self.name_type]
        return name_type

    def get_date_display(self):
        """Get the date display labels according to the Name's
        name type

        See Name.DATE_DISPLAY_LABELS
        """
        return self.DATE_DISPLAY_LABELS.get(self.name_type)

    def has_current_location(self):
        """True if the Name has a current location in the location_set."""
        return self.location_set.current_location is not None

    def has_geocode(self):
        """True if the instance has one or more related Locations."""
        if self.location_set.count():
            return True
        else:
            return False
    has_geocode.boolean = True  # Enables icon display in the Django admin.

    def has_schema_url(self):
        """True if the instance has a schema url."""
        return self.get_schema_url() is not None

    def _is_name_type(self, type_id):
        """Test if the instance of Name is a certain
        Name Type.

        Accepts the id of the Name Type, and returns a boolean.
        """
        return type_id == self.name_type

    def is_personal(self):
        """True if the Name has the Name Type Personal."""
        return self._is_name_type(self.PERSONAL)

    def is_organization(self):
        """True if the Name has the Name Type Organization."""
        return self._is_name_type(self.ORGANIZATION)

    def is_event(self):
        """True if the Name has the Name Type Event."""
        return self._is_name_type(self.EVENT)

    def is_software(self):
        """True if the Name has the Name Type Software."""
        return self._is_name_type(self.SOFTWARE)

    def is_building(self):
        """True if the Name has the Name Type Building."""
        return self._is_name_type(self.BUILDING)

    def _is_record_status(self, status_id):
        """Test if the instance of Name has a particular
        record_status.

        Accepts the id of the Name Type, and returns a boolean.
        """
        return status_id == self.record_status

    def is_active(self):
        """True if the Name has the Active status."""
        return self._is_record_status(self.ACTIVE)

    def is_deleted(self):
        """True if the Name has the Deleted status."""
        return self._is_record_status(self.DELETED)

    def is_suppressed(self):
        """True if the Name has the Suppressed status."""
        return self._is_record_status(self.SUPPRESSED)

    def render_biography(self):
        """Render the Markdown biography to HTML."""
        return markdown2.markdown(self.biography)

    def __normalize_name(self):
        """Normalize the name attribute and assign it the normalized_name
        attribute.
        """
        self.normalized_name = normalizeSimplified(self.name)

    def __find_location(self):
        """Use the normalized_name attribute and the Location.URL to
        attempt to find the instance's location.

        A location is only attached if the server responds with a single
        result.
        """
        URL_RESOURCE = 'http://maps.googleapis.com/maps/api/geocode/json'
        URL_QUERY_TEMPLATE = '?address={address}&sensor=true'
        URL = URL_RESOURCE + URL_QUERY_TEMPLATE

        url = URL.format(address=quote(self.normalized_name))
        payload = json.load(urlopen(url))

        # Only add the location if the Name matched one and only one
        # location from the API.
        if payload.get('status') == "OK" and len(payload.get('results')) == 1:
            coordinate = payload['results'][0]['geometry']['location']
            self.location_set.create(latitude=coordinate['lat'],
                                     longitude=coordinate['lng'])

    def __assign_name_id(self):
        """Use the BaseTicketing object to assign a name_id."""
        if not self.name_id:
            self.name_id = unicode(BaseTicketing.objects.create())

    def save(self, **kwargs):
        self.__normalize_name()
        self.__assign_name_id()
        super(Name, self).save()
        if self.is_building() and not self.location_set.count():
            self.__find_location()

    def clean(self, *args, **kwargs):
        # Call merged_with_validator here so that we can pass in
        # the model instance.
        validate_merged_with(self)
        super(Name, self).clean(*args, **kwargs)

    def __unicode__(self):
        return self.name_id

    class Meta:
        ordering = ['name']
        unique_together = (('name', 'name_id'),)


class LocationManager(models.Manager):
    """Custom Manager for the Location model."""
    use_for_related_fields = True

    def _get_current_location(self):
        """Filters through a Name object's related locations and
        returns the one marked as current.
        """
        return self.get_queryset().filter(status=self.model.CURRENT).first()

    # Makes the current location available as a property on
    # the RelatedManager.
    current_location = property(_get_current_location)


class Location(models.Model):
    """Defines the location of a related Name model instance."""
    CURRENT = 0
    FORMER = 1

    LOCATION_STATUS_CHOICES = (
        (CURRENT, 'current'),
        (FORMER, 'former')
    )

    HELP_TEXT = """
    <strong>
        <a target="_blank" href="http://itouchmap.com/latlong.html">
            iTouchMap
        </a>
        : this service might be useful for filling in the lat/long data
    </strong>
    """

    belong_to_name = models.ForeignKey('Name')

    latitude = models.DecimalField(
        max_digits=13,
        decimal_places=10,
        help_text=HELP_TEXT)

    longitude = models.DecimalField(
        max_digits=13,
        decimal_places=10,
        help_text=HELP_TEXT)

    status = models.IntegerField(
        choices=LOCATION_STATUS_CHOICES,
        default=CURRENT)

    objects = LocationManager()

    class Meta:
        ordering = ['status']

    def geo_point(self):
        return '{lat} {lng}'.format(lat=self.latitude, lng=self.longitude)

    def is_current(self):
        """True if the Location has a status of Current."""
        return self.CURRENT == self.status

    def save(self, **kwargs):
        super(Location, self).save()
        # When this instance's status is CURRENT, get all other locations
        # related the belong_to_name, and set the status to FORMER.
        if self.is_current():
            former_locs = self.belong_to_name.location_set.exclude(id=self.id)
            for l in former_locs:
                l.status = self.FORMER
                l.save()

    def __unicode__(self):
        return self.geo_point()
