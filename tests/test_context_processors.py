import pytest

from name.context_processors import name_types
from name.models import NAME_TYPE_CHOICES


def test_name_types(rf):
    """Verify that the name_types processors add the NAME_TYPES_CHOICES
    to the passed in request.
    """
    request = rf.get('/')
    context = name_types(request)
    assert dict(NAME_TYPE_CHOICES) == context['name_types']


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
    assert dict(NAME_TYPE_CHOICES) == request.context['name_types']
