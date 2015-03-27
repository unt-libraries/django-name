import pytest
import json
import random

from django.core.urlresolvers import reverse
from name import models


@pytest.fixture
def name_fixture(db, scope="module"):
    return models.Name.objects.create(
        name='test person',
        name_type=0,
        begin='2012-01-12')


@pytest.fixture
def merged_name_fixtures(db, scope="module"):
    name1 = models.Name.objects.create(name='test person 1', name_type=0)
    name2 = models.Name.objects.create(name='test person 2', name_type=0)
    name1.merged_with = name2
    name1.save()
    return (name1, name2)


@pytest.fixture
def twenty_name_fixtures(db, scope="module"):
    for x in range(21):
        models.Name.objects.create(
            name="Name {}".format(x),
            name_type=random.randint(0, 4),
            begin='2012-01-12')
    return models.Name.objects.all()


@pytest.mark.django_db
def test_entry_detail_returns_ok(client, name_fixture):
    response = client.get(
        reverse('name_entry_detail', args=[name_fixture.name_id]))
    assert 200 == response.status_code


@pytest.mark.django_db
def test_entry_detail_returns_gone(client, name_fixture):
    name_fixture.record_status = 1
    name_fixture.save()
    response = client.get(
        reverse('name_entry_detail', args=[name_fixture.name_id]))
    assert 410 == response.status_code


@pytest.mark.django_db
def test_entry_detail_returns_not_found(client, name_fixture):
    name_fixture.record_status = 2
    name_fixture.save()
    response = client.get(
        reverse('name_entry_detail', args=[name_fixture.name_id]))
    assert 404 == response.status_code


@pytest.mark.django_db
def test_merged_entry_detail_returns_ok(client, merged_name_fixtures):
    merged, primary = merged_name_fixtures
    response = client.get(
        reverse('name_entry_detail', args=[primary.name_id]))
    assert 200 == response.status_code


@pytest.mark.django_db
def test_merged_entry_detail_returns_redirect(client, merged_name_fixtures):
    merged, primary = merged_name_fixtures
    response = client.get(
        reverse('name_entry_detail', args=[merged.name_id]))
    assert 302 == response.status_code


@pytest.mark.django_db
def test_mads_serialize_returns_ok(client, name_fixture):
    response = client.get(
        reverse('name_mads_serialize', args=[name_fixture.name_id]))
    assert 200 == response.status_code


@pytest.mark.django_db
def test_label_returns_redirected(client, name_fixture):
    response = client.get(
        reverse('name_label', args=[name_fixture.name]))
    assert 302 == response.status_code


@pytest.mark.django_db
def test_label_returns_not_found_without_query(client):
    response = client.get(
        reverse('name_label', args=['']))
    assert 404 == response.status_code
    assert 'No matching term found' not in response.content


@pytest.mark.django_db
def test_label_returns_not_found_with_query(client):
    response = client.get(
        reverse('name_label', args=['&&&&&&&&']))
    assert 404 == response.status_code
    assert 'No matching term found' in response.content


@pytest.mark.django_db
def test_export(client, name_fixture):
    response = client.get(reverse('name_export'))
    assert 200 == response.status_code


def test_opensearch(client):
    response = client.get(reverse('name_opensearch'))
    assert 200 == response.status_code


@pytest.mark.django_db
def test_feed(client):
    response = client.get(reverse('name_feed'))
    assert 200 == response.status_code


def test_about(client):
    response = client.get(reverse('name_about'))
    assert 200 == response.status_code


@pytest.mark.django_db
def test_stats_returns_ok(client, name_fixture):
    response = client.get(reverse('name_stats'))
    assert 200 == response.status_code


# TODO: This should not throw a 500
@pytest.mark.xfail
@pytest.mark.django_db
def test_stats_returns_ok_with_no_names(client):
    response = client.get(reverse('name_stats'))
    assert 200 == response.status_code


@pytest.mark.django_db
def test_get_names_returns_ok(client):
    response = client.get(reverse('name_names'))
    assert 200 == response.status_code


# TODO: Look at ways that we can confirm that the
# requests was received as an Ajax call
@pytest.mark.django_db
def test_get_names_xhr_returns_ok(client):
    response = client.get(
        reverse('name_names'),
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    assert 200 == response.status_code


@pytest.mark.django_db
def test_get_names_xhr_returns_only_10_names(client, twenty_name_fixtures):
    response = client.get(
        reverse('name_names'),
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    names = json.loads(response.content)
    assert len(names) == 10


# TODO: Take another look at this. We might not need
#       Allow-Headers on every request, perhaps only ajax
# TODO: Find a way to test that the origin header is set to '*'
@pytest.mark.django_db
def test_get_names_has_cors_headers(client):
    response = client.get(reverse('name_names'))
    assert response.has_header('Access-Control-Allow-Origin')
    assert response.has_header('Access-Control-Allow-Headers')


@pytest.mark.django_db
def test_landing(client):
    response = client.get(reverse('name_landing'))
    assert 200 == response.status_code


@pytest.mark.django_db
def test_name_json_returns_ok(client, name_fixture):
    response = client.get(reverse('name_json', args=[name_fixture]))
    assert 200 == response.status_code


# TODO: This should not return a 500
@pytest.mark.xfail
@pytest.mark.django_db
def test_name_json_handles_unknown_name(client):
    response = client.get(reverse('name_json', args=[0]))
    assert 404 == response.status_code


# TODO: Move this to test_search.py
@pytest.mark.django_db
def test_search_with_q(client, twenty_name_fixtures):
    name = twenty_name_fixtures.first()
    url = reverse('name_search') + "?q={}".format(name.name)
    response = client.get(url)
    assert name.name in response.content


# TODO: Move this to test_search.py
@pytest.mark.xfail
def test_search_with_q_type(client, name_fixture):
    assert False


# TODO: Move this to test_search.py
@pytest.mark.xfail
def test_search_without_query(client):
    assert False
