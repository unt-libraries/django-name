from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse_lazy
from django.utils.feedgenerator import Atom1Feed

from . import app_settings
from .models import Name


class NameAtomFeedType(Atom1Feed):
    """Create an Atom feed that sets the Content-Type response
    header to application/xml.
    """
    mime_type = 'application/xml'


class NameAtomFeed(Feed):
    feed_type = NameAtomFeedType
    link = reverse_lazy("name_feed")
    title = "Name App"
    subtitle = "New Name Records"
    author_name = app_settings.NAME_FEED_AUTHOR_NAME
    author_email = app_settings.NAME_FEED_AUTHOR_EMAIL
    author_link = app_settings.NAME_FEED_AUTHOR_LINK

    def items(self):
        # last 5 added items
        return Name.objects.order_by('-date_created')[:20]

    def item_title(self, obj):
        return obj.name

    def item_description(self, obj):
        return 'Name Type: {0}'.format(obj.get_name_type_label())

    def item_link(self, obj):
        return obj.get_absolute_url()
