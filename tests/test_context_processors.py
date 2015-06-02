import pytest

from name.context_processors import name_types, branding
from name.models import Name
from name import app_settings


def test_name_types(rf):
    """Verify that the name_types processors add the NAME_TYPES_CHOICES
    to the passed in request.
    """
    request = rf.get('/')
    context = name_types(request)
    assert dict(Name.NAME_TYPE_CHOICES) == context['name_types']


@pytest.mark.django_db
def test_name_types_in_request(client):
    """Verify that the NAME_TYPE_CHOICES are present when the
    context processors are enabled.

    The name_type context processor is already added to the test project.
    See tests/settings/base.py

    We use the client made available by pytest-django to get a request
    that has already processed.
    """
    request = client.get('/name/')
    assert dict(Name.NAME_TYPE_CHOICES) == request.context['name_types']


def test_branding(rf):
    """Verify that the branding processor adds the NAME_APP_TITLE
    and NAME_ADMIN_EMAIL to the passed in request.
    """
    request = rf.get('/')
    context = branding(request)
    assert context['name_app_title'] == app_settings.NAME_APP_TITLE
    assert context['name_admin_email'] == app_settings.NAME_ADMIN_EMAIL


@pytest.mark.django_db
def test_branding_is_added_to_request(client):
    """Verify that the `name_app_title` and `name_admin_email` keys
    are present when the context processors are enabled.

    The branding context processor is already added to the test project.
    See tests/settings/base.py
    """
    request = client.get('/name/')
    assert 'name_app_title' in request.context
    assert 'name_admin_email' in request.context
