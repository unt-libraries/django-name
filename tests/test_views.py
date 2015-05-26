import pytest
import json
from name.models import Location, Name

from django.core.urlresolvers import reverse

# Give all tests access to the database.
pytestmark = pytest.mark.django_db


def test_entry_detail_returns_ok(client, name_fixture):
    response = client.get(
        reverse('name_entry_detail', args=[name_fixture.name_id]))
    assert 200 == response.status_code


def test_entry_detail_returns_gone(client, name_fixture):
    name_fixture.record_status = 1
    name_fixture.save()
    response = client.get(
        reverse('name_entry_detail', args=[name_fixture.name_id]))
    assert 410 == response.status_code


def test_entry_detail_returns_not_found(client, name_fixture):
    name_fixture.record_status = 2
    name_fixture.save()
    response = client.get(
        reverse('name_entry_detail', args=[name_fixture.name_id]))
    assert 404 == response.status_code


def test_merged_entry_detail_returns_ok(client, merged_name_fixtures):
    merged, primary = merged_name_fixtures
    response = client.get(
        reverse('name_entry_detail', args=[primary.name_id]))
    assert 200 == response.status_code


def test_merged_entry_detail_returns_redirect(client, merged_name_fixtures):
    merged, primary = merged_name_fixtures
    response = client.get(
        reverse('name_entry_detail', args=[merged.name_id]))
    assert 302 == response.status_code


def test_label_returns_redirected(client, name_fixture):
    response = client.get(
        reverse('name_label', args=[name_fixture.name]))
    assert 302 == response.status_code


def test_label_returns_not_found_without_query(client):
    """Test label returns Not Found without a query.

    This will fail if label does not return with a status
    code of 404.
    """
    response = client.get(
        reverse('name_label', args=['']))
    assert 404 == response.status_code
    assert 'No matching term found' not in response.content


def test_label_returns_not_found_with_query(client):
    """Test label returns Not Found with a query that does not
    match anything.

    This will fail if label does not return with a status
    code of 404.
    """
    response = client.get(
        reverse('name_label', args=['&&&&&&&&']))
    assert 404 == response.status_code
    assert 'No matching term found' in response.content


def test_label_returns_not_found_multiple_names_found(client):
    name_name = "John Smith"
    Name.objects.create(name=name_name, name_type=0)
    Name.objects.create(name=name_name, name_type=0)

    response = client.get(
        reverse('name_label', args=[name_name]))
    assert 404 == response.status_code
    assert 'There are multiple Name objects with' in response.content


def test_export(client, name_fixture):
    response = client.get(reverse('name_export'))
    assert 200 == response.status_code


def test_opensearch(client):
    response = client.get(reverse('name_opensearch'))
    assert 200 == response.status_code


def test_feed(client):
    response = client.get(reverse('name_feed'))
    assert 200 == response.status_code


def test_about(client):
    response = client.get(reverse('name_about'))
    assert 200 == response.status_code


def test_stats_returns_ok(client, name_fixture):
    response = client.get(reverse('name_stats'))
    assert 200 == response.status_code


def test_stats_returns_ok_with_no_names(client):
    response = client.get(reverse('name_stats'))
    assert 200 == response.status_code


def test_get_names_returns_ok(client):
    response = client.get(reverse('name_names'))
    assert 200 == response.status_code


def test_get_names_xhr_returns_ok(client):
    response = client.get(
        reverse('name_names'),
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    assert 200 == response.status_code


def test_get_names_xhr_returns_only_10_names(client, twenty_name_fixtures):
    response = client.get(
        reverse('name_names'),
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    names = json.loads(response.content)
    assert len(names) == 10


def test_get_names_has_cors_headers(client):
    response = client.get(reverse('name_names'))
    assert response.has_header('Access-Control-Allow-Origin')
    assert response.has_header('Access-Control-Allow-Headers')
    assert response['Access-Control-Allow-Origin'] == '*'


def test_landing(client):
    response = client.get(reverse('name_landing'))
    assert 200 == response.status_code


def test_landing_does_not_count_inactive_names(client, status_name_fixtures):
    """Checks that only active names are counted.

    The status_name_fixture supplies this test with 3 Name objects of each
    Name type, where only one of each Name type is active.
    """
    response = client.get(reverse('name_landing'))
    context = response.context[-1]['counts']
    assert 1 == context['personal']
    assert 1 == context['building']
    assert 1 == context['event']
    assert 1 == context['organization']
    assert 1 == context['software']
    assert 5 == context['total']


def test_name_json_returns_ok(client, name_fixture):
    response = client.get(reverse('name_json', args=[name_fixture]))
    assert 200 == response.status_code


def test_name_json_handles_unknown_name(client):
    response = client.get(reverse('name_json', args=[0]))
    assert 404 == response.status_code


def test_map_returns_ok(client):
    response = client.get(reverse('name_map'))
    assert 200 == response.status_code


def test_map_json_xhr_returns_payload(client):
    name = Name.objects.create(name="Test", name_type=0)

    Location.objects.create(
        status=0,
        latitude=33.210241,
        longitude=-97.148857,
        belong_to_name=name)

    response = client.get(
        reverse('name_map_json'),
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    assert name.name_id in response.content
    assert json.loads(response.content)


def test_map_json_xhr_returns_with_no_locations(client, twenty_name_fixtures):
    response = client.get(
        reverse('name_map_json'),
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    assert response.context is None
    assert response.status_code == 200


def test_map_json_returns_not_found(client, twenty_name_fixtures):
    response = client.get(reverse('name_map_json'))
    assert response.status_code == 404


def test_stats_json_returns_ok_with_no_names(client):
    response = client.get(reverse('name_stats_json'))
    assert response.status_code == 200


def test_stats_json_returns_ok(client, search_fixtures):
    response = client.get(reverse('name_stats_json'))
    assert response.status_code == 200


def test_stats_json_json_data(client, search_fixtures):
    response = client.get(reverse('name_stats_json'))
    data = json.loads(response.content)
    assert data.get('created', False)
    assert data.get('modified', False)
    assert data.get('name_type_totals', False)
