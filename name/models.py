from django.db import models, connections, transaction
from NACO import normalizeSimplified
from django.core.exceptions import ValidationError
import requests
try:
    # the json module was included in the stdlib in python 2.6
    # http://docs.python.org/library/json.html
    import json
except ImportError:
    # simplejson 2.0.9 is available for python 2.4+
    # http://pypi.python.org/pypi/simplejson/2.0.9
    # simplejson 1.7.3 is available for python 2.3+
    # http://pypi.python.org/pypi/simplejson/1.7.3
    import simplejson as json

NOTE_TYPE_CHOICES = (
    (0, 'Biographical/Historical'),
    (1, 'Deletion Information'),
    (2, 'Nonpublic'),
    (3, 'Source'),
    (4, 'Other'),
)
RECORD_STATUS_CHOICES = (
    (0, 'Active'),
    (1, 'Deleted'),
    (2, 'Suppressed'),
)
NAME_TYPE_CHOICES = (
    (0, 'Personal'),
    (1, 'Organization'),
    (2, 'Event'),
    (3, 'Software'),
    (4, 'Building'),
)
DATE_DISPLAY_LABELS = {
    0: {
        'type': 'Personal',
        'begin': 'Date of Birth',
        'end': 'Date of Death'
    },
    1: {
        'type': 'Organization',
        'begin': 'Founded Date',
        'end': 'Defunct'
    },
    2: {
        'type': 'Event',
        'begin': 'Begin Date',
        'end': 'End Date'
    },
    3: {
        'type': 'Software',
        'begin': 'Begin Date',
        'end': 'End Date'
    },
    4: {
        'type': 'Building',
        'begin': 'Erected Date',
        'end': 'Demolished Date',
    },
    None: {
        'type': None,
        'begin': 'Born/Founded Date',
        'end': 'Died/Defunct Date'
    },
}
VARIANT_TYPE_CHOICES = (
    (0, 'Acronym'),
    (1, 'Abbreviation'),
    (2, 'Translation'),
    (3, 'Expansion'),
    (4, 'Other'),
)
LOCATION_STATUS_CHOICES = (
    (0, "current"),
    (1, "former"),
)


class Identifier_Type(models.Model):
    label = models.CharField(
        max_length=255,
        help_text="What kind of data is this? Personal website? Twitter?",
    )
    icon_path = models.CharField(
        max_length=255,
        blank=True,
        help_text="Path to icon image?",
    )
    homepage = models.URLField(
        blank=True,
        help_text="Homepage of label. Twitter.com, Facebook.com, etc",
    )

    class Meta:
        ordering = ["label"]
        verbose_name = "Identifier Type"

    def __unicode__(self):
        return self.label


class Identifier(models.Model):
    type = models.ForeignKey(
        "Identifier_Type",
        help_text="Catagorize this record's identifiers here",
    )
    belong_to_name = models.ForeignKey("Name")
    value = models.CharField(max_length=500)
    visible = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order", "type"]

    def __unicode__(self):
        return self.value


class Note(models.Model):
    note = models.TextField(help_text="Enter notes about this record here")
    note_type = models.IntegerField(choices=NOTE_TYPE_CHOICES)
    belong_to_name = models.ForeignKey("Name")

    def __unicode__(self):
        return self.note


class Variant(models.Model):
    belong_to_name = models.ForeignKey("Name")
    variant_type = models.IntegerField(
        max_length=50,
        choices=VARIANT_TYPE_CHOICES,
        help_text="Choose variant type.",
    )
    variant = models.CharField(
        max_length=255,
        help_text="Fill in the other name variants, if any.",
    )
    normalized_variant = models.CharField(
        max_length=255,
        help_text="NACO normalized variant text",
        editable=False,
    )

    def save(self):

        self.normalized_variant = normalizeSimplified(self.variant)
        super(Variant, self).save()

    def __unicode__(self):
        return self.variant


class TicketingManager(models.Manager):

    def create(self, *args, **kwargs):
        obj, created = self.get_or_create(stub=self.model.STUB_DEFAULT)
        if not created:
            with transaction.atomic():
                obj.delete()
                obj = self.create(stub=self.model.STUB_DEFAULT)
        return obj


class BaseTicketing(models.Model):

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
        return u'nm%07d' % self.ticket


def validate_merged_with(value):
    """
    Custom validator for the merged with CharField.
    We don't want to allow users to do an infinite redirect loop b/c of
    merging a record that is already merged with the current record
    """

    try:
        # attempt to set the variables to their values
        to_be_merged = 'nm%07d' % value
        current = str(Name.objects.get(name_id=to_be_merged).merged_with)
        current_merged = str(Name.objects.get(name_id=current).merged_with)
    except Exception, e:
        # make the comparison variables different to ensure test failure
        current_merged = '1'
        to_be_merged = '2'

    # test if they are looped
    if current_merged == to_be_merged:
        raise ValidationError(
            u'can\'t merge a record into an infinite redirect loop'
        )


class Name(models.Model):
    """
    The record model defines the information stored by the name app
    Each record has a unique name identifier associated with it which is
    implemented as UUID.
    """

    # only one name per record
    name = models.CharField(
        max_length=255,
        help_text="Please use the general reverse order: LAST, FIRST",
    )

    normalized_name = models.CharField(
        max_length=255,
        help_text="NACO normalized form of the name",
        editable=False,
    )

    # the name must be one of a certain type, currently 4 choices
    name_type = models.IntegerField(
        max_length=1,
        choices=NAME_TYPE_CHOICES,
        help_text="Must be one of 4 types",
    )

    # date, month or year of birth or incorporation of the name
    begin = models.CharField(
        max_length=25,
        blank=True,
        help_text="Conforms to EDTF format YYYY-MM-DD",
    )

    # date, month of year of death or un-incorporation of the name
    end = models.CharField(
        max_length=25,
        blank=True,
        help_text="Conforms to EDTF format YYYY-MM-DD",
    )

    # MusicBrainz derived
    disambiguation = models.CharField(
        max_length=255,
        blank=True,
        help_text="Clarify to whom or what this record pertains."
    )

    # bio text - formatted with _markdown_ markup
    biography = models.TextField(
        blank=True,
        help_text="Compatible with MARKDOWN",
    )

    # record status flag (active / merged / etc)
    record_status = models.IntegerField(
        choices=RECORD_STATUS_CHOICES,
        default="0",
    )

    # if marked merged, value is record id of target to merge with
    merged_with = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        related_name='merged_with_name',
        validators=[validate_merged_with],
    )

    # automatically generate created date
    date_created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    # update when we change the record
    last_modified = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    # auto incrementing from nameid
    name_id = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
    )

    def has_geocode(self):
        l = Location.objects.filter(belong_to_name=self)
        if len(l) > 0:
            return True
        else:
            return False
    # this enables icon display on the django admin rather than textual "T/F"
    has_geocode.boolean = True

    def save(self, **kwargs):
        if not self.name_id:
            self.name_id = unicode(BaseTicketing.objects.create())
        self.normalized_name = normalizeSimplified(self.name)
        super(Name, self).save()
        if self.name_type == 4 and Location.objects.filter(belong_to_name=self).count() == 0:
            url = 'http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=true' % self.normalized_name
            search_json = json.loads(requests.get(url).content)
            if search_json['status'] == 'OK' and len(search_json['results']) == 1:
                Location.objects.create(
                    belong_to_name=self,
                    latitude=search_json['results'][0]['geometry']['location']['lat'],
                    longitude=search_json['results'][0]['geometry']['location']['lng'],
                )

    def __unicode__(self):
        return self.name_id

    class Meta:
        ordering = ["name"]


class Location(models.Model):
    belong_to_name = models.ForeignKey("Name")
    latitude = models.DecimalField(
        max_digits=13,
        decimal_places=10,
        help_text="""
        <strong><a target="_blank" href="http://itouchmap.com/latlong.html">iTouchMap</a>: this service might be useful for filling in the lat/long data</strong>
        """,
    )
    longitude = models.DecimalField(
        max_digits=13,
        decimal_places=10,
        help_text="""
        <strong><a target="_blank" href="http://itouchmap.com/latlong.html">iTouchMap</a>: this service might be useful for filling in the lat/long data</strong>
        """,
    )
    status = models.IntegerField(max_length=2, choices=LOCATION_STATUS_CHOICES, default=0)

    class Meta:
        ordering = ["status"]

    @property
    def geo_point(self):
        return "%s, %s" (str(self.latitude), str(self.longitude))

    def save(self, **kwargs):
        super(Location, self).save()
        # if we change this location to the current location, all other
        # locations that belong to the same name should be changed to former.
        if self.status == 0:
            former_locs = Location.objects.filter(belong_to_name=self.belong_to_name).exclude(pk=self.pk)
            for l in former_locs:
                l.status = 1
                l.save()
