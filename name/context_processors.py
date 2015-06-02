from .models import Name
from . import app_settings


def name_types(request):
    return {'name_types': dict(Name.NAME_TYPE_CHOICES)}


def branding(request):
    return {
        'name_app_title': app_settings.NAME_APP_TITLE,
        'name_admin_email': app_settings.NAME_ADMIN_EMAIL
    }
