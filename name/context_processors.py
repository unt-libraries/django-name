from .models import Name
from . import app_settings


def name(request):
    """Adds the Name Types and branding options to the request
    context.
    """
    return {
        'name_types': dict(Name.NAME_TYPE_CHOICES),
        'name_app_title': app_settings.NAME_APP_TITLE,
        'name_admin_email': app_settings.NAME_ADMIN_EMAIL
    }
