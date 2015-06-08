from django.conf import settings

from . import __title__

# App level settings for the Name feed.
NAME_FEED_AUTHOR_NAME = getattr(settings, 'NAME_FEED_AUTHOR_NAME', __title__)

NAME_FEED_AUTHOR_EMAIL = getattr(settings, 'NAME_FEED_AUTHOR_EMAIL', None)

NAME_FEED_AUTHOR_LINK = getattr(settings, 'NAME_FEED_AUTHOR_LINK', None)

# App level settings for custom branding.
NAME_APP_TITLE = getattr(settings, 'NAME_APP_TITLE', __title__)

NAME_ADMIN_EMAIL = getattr(settings, 'NAME_ADMIN_EMAIL', None)
