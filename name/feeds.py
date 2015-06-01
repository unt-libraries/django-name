from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse_lazy
from django.utils.feedgenerator import Atom1Feed

from . import app_settings
from .models import Name


class NameAtomFeedType(Atom1Feed):
    """Custom Atom Feed Type for Name objects.

    This will set the Content-Type header to application/xml, and
    add a georss:point element to any entry that has a current location
    set.
    """
    mime_type = 'application/xml'
    GEO_RSS_NS = 'http://www.georss.org/georss'

    def root_attributes(self):
        attrs = super(NameAtomFeedType, self).root_attributes()
        attrs['xmlns:georss'] = self.GEO_RSS_NS
        return attrs

    def add_item_elements(self, handler, item):
        super(NameAtomFeedType, self).add_item_elements(handler, item)

        # Add the georss:point element if the item has a geo_point
        # attribute.
        geo_point = item.get('geo_point', None)
        if geo_point:
            handler.addQuickElement('georss:point', geo_point)


class NameAtomFeed(Feed):
    """Atom Feed for Name objects."""
    feed_type = NameAtomFeedType
    link = reverse_lazy("name:feed")
    title = "Name App"
    subtitle = "New Name Records"

    author_name = app_settings.NAME_FEED_AUTHOR_NAME
    author_email = app_settings.NAME_FEED_AUTHOR_EMAIL
    author_link = app_settings.NAME_FEED_AUTHOR_LINK

    def items(self):
        return Name.objects.order_by('-date_created')[:20]

    def item_title(self, obj):
        return obj.name

    def item_description(self, obj):
        return 'Name Type: {0}'.format(obj.get_name_type_label())

    def item_link(self, obj):
        return obj.get_absolute_url()

    def item_updateddate(self, obj):
        return obj.last_modified

    def item_location(self, obj):
        if obj.has_current_location():
            return obj.location_set.current_location.geo_point()

    def item_extra_kwargs(self, obj):
        return {u'geo_point': self.item_location(obj)}
