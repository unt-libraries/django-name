import pytest
import json

from django.core.urlresolvers import reverse

# All test need access to the database in this file.
pytestmark = pytest.mark.django


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


def test_search_with_q(client, twenty_name_fixtures):
    '''Search with q only. No name_types provided'''
    name = twenty_name_fixtures.first()
    url = reverse('name_search') + "?q={}".format(name.name)
    response = client.get(url)
    assert name.name in response.content


# FIXME: Currently, there is not a reliable way to test for the amount of
#       of names, or of which type they are. After some template updates
#       this may be possible.
@pytest.mark.xfail(reason="No Test")
def test_search_with_q_type(rf, twenty_name_fixtures):
    assert False


# FIXME: Currently, there is not a reliable way to test for the amount of
#       of names, or of which type they are. After some template updates
#       this may be possible.
@pytest.mark.xfail(reason="No Test")
def test_search_without_query(client):
    assert False
