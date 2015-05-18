from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from . import app_settings
from .models import Name, Location


class NameAtomFeedType(Atom1Feed):
    """Create an Atom feed that sets the Content-Type response
    header to application/xml.
    """
    mime_type = 'application/xml'


class NameAtomFeed(Feed):
    feed_type = NameAtomFeedType
    link = "/name/feed/"
    title = "Name App"
    subtitle = "New Name Records"
    author_name = app_settings.NAME_FEED_AUTHOR_NAME
    author_email = app_settings.NAME_FEED_AUTHOR_EMAIL
    author_link = app_settings.NAME_FEED_AUTHOR_LINK

    def items(self):
        # last 5 added items
        return Name.objects.order_by('-date_created')[:20]

    def item_title(self, item):
        return item.name

    def item_location(self, item):
        """
        Returns an extra keyword arguments dictionary that is used
        with the `add_item` call of the feed generator. Add the
        'content' field of the 'Entry' item, to be used by the custom
        feed generator.
        """
        location_set = []
        for l in Location.objects.filter(belong_to_name=item):
            location_set.append(
                'georss:point', "%s %s" % (l.latitude, l.longitude)
            )
        return location_set

    def item_description(self, item):
        return "Name Type: %s" % item.get_name_type_label()

    def item_link(self, item):
        return item.get_absolute_url()
