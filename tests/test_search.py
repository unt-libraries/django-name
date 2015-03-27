import pytest
import json

from name.models import Name
from django.core.urlresolvers import reverse

# All test need access to the database in this file.
pytestmark = pytest.mark.django


@pytest.fixture
def name_fixtures(db, scope="module"):
    Name.objects.create(name='test person',
                        name_type=0, begin='2012-01-12')
    Name.objects.create(name='test organization',
                        name_type=1, begin='2000-01-12')
    Name.objects.create(name='test event',
                        name_type=2, begin='2500-01-12')
    Name.objects.create(name='test building',
                        name_type=4, begin='2000-01-12')

query_template = '?q_type={0}&q={1}'


def test_json_returns_expected_results(client, name_fixtures):
    query = query_template.format('Personal', 'person')
    response = client.get(reverse('name_names') + query)

    assert json.loads(response.content)[0]['name'] == 'test person'
    assert response.status_code is 200


def test_can_json_search_multiple_name_types(client, name_fixtures):
    query = query_template.format('Personal,Organization', 'test')
    response = client.get(
        reverse('name_names') + query)
    json_results = json.loads(response.content)

    assert len(json_results) is 2
    assert response.status_code is 200


def test_can_search(client, name_fixtures):
    query = query_template.format('Personal', 'test')
    response = client.get(reverse('name_search') + query)
    assert response.status_code is 200


def test_can_search_multiple_name_types(client, name_fixtures):
    query = query_template.format('Personal,Organization', 'test')
    response = client.get(
        reverse('name_search') + query)

    assert response.status_code is 200
