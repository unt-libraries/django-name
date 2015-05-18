from django.conf import settings

NAME_FEED_AUTHOR_NAME = getattr(settings, 'NAME_FEED_AUTHOR_NAME', None)

NAME_FEED_AUTHOR_EMAIL = getattr(settings, 'NAME_FEED_AUTHOR_EMAIL', None)

NAME_FEED_AUTHOR_LINK = getattr(settings, 'NAME_FEED_AUTHOR_LINK', None)
