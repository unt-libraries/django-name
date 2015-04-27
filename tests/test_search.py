import pytest
import json

from django.core.urlresolvers import reverse

# All test need access to the database in this file.
pytestmark = pytest.mark.django


query_template = '?q_type={0}&q={1}'


def test_json_search_returns_expected_results(client, name_fixtures):
    """Test that the search returns the Name object that was searched for
    and that the status code is 200.
    """
    query = query_template.format('Personal', 'person')
    response = client.get(reverse('name_names') + query)

    assert response.status_code is 200
    assert json.loads(response.content)[0]['name'] == 'test person'


def test_json_search_with_multiple_name_types(client, name_fixtures):
    query = query_template.format('Personal,Organization', 'test')
    response = client.get(
        reverse('name_names') + query)
    json_results = json.loads(response.content)

    assert response.status_code is 200
    assert len(json_results) is 2


def test_can_search(client, name_fixtures):
    """Test the HTML search returns correctly."""
    query = query_template.format('Personal', 'test')
    response = client.get(reverse('name_search') + query)
    assert response.status_code is 200


def test_search_multiple_name_types(client, name_fixtures):
    query = query_template.format('Personal,Organization', 'test')
    response = client.get(
        reverse('name_search') + query)

    assert response.status_code is 200


def test_search_with_q(client, twenty_name_fixtures):
    """Search with q only. No name_types provided."""
    name = twenty_name_fixtures.first()
    url = reverse('name_search')
    response = client.get(url, {'q': name.name})
    entries = response.context[-1]['entries']
    assert name in entries.object_list


def test_search_with_q_type(client, search_fixtures):
    url = reverse('name_search')
    response = client.get(url, {'q_type': 'Personal'})
    entries = response.context[-1]['entries']
    assert len(entries.object_list) == 4
    assert all(x.is_personal() for x in entries.object_list)


def test_search_with_two_q_types(client, search_fixtures):
    url = reverse('name_search')
    response = client.get(url, {'q_type': 'Personal,Event'})
    entries = response.context[-1]['entries']
    assert len(entries.object_list) == 8
    assert all(x.is_personal() or x.is_event() for x in entries.object_list)


def test_search_without_query(client, search_fixtures):
    url = reverse('name_search')
    response = client.get(url)
    entries = response.context[-1]['entries']
    assert entries is None
