import pytest

from django.core.urlresolvers import reverse
from name import models


@pytest.fixture
def name_fixture(db, scope="module"):
    return models.Name.objects.create(
        name='test person',
        name_type=0,
        begin='2012-01-12')


@pytest.mark.django_db
def test_entry_detail_returns_ok(client, name_fixture):
    response = client.get(
        reverse('name_entry_detail', args=[name_fixture.name_id]))
    assert 200 == response.status_code


@pytest.mark.xfail
def test_merged_entry_detail_returns_not_found(client):
    assert False


@pytest.mark.xfail
def test_merged_entry_detail_returns_gone(client):
    assert False


@pytest.mark.xfail
def test_merged_entry_detail_returns_ok(client):
    assert False


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
def test_label_returns_not_found(client):
    response = client.get(
        reverse('name_label', args=['']))
    assert 404 == response.status_code


@pytest.mark.django_db
def test_export(client, name_fixture):
    response = client.get(reverse('name_export'))
    assert 200 == response.status_code


def test_opensearch(client):
    response = client.get(reverse('name_opensearch'))
    assert 200 == response.status_code


def test_about(client):
    response = client.get(reverse('name_about'))
    assert 200 == response.status_code


@pytest.mark.django_db
def test_stats_returns_ok(client, name_fixture):
    response = client.get(reverse('name_stats'))
    assert 200 == response.status_code


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


# TODO: Take another look at this. We might not need
#       Allow-Headers on every request, perhaps only ajax
# TODO: Find a way to test that the origin header is set to '*'
@pytest.mark.xfail
@pytest.mark.django_db
def test_get_names_has_cors_headers(client):
    response = client.get(reverse('name_names'))
    assert response.has_header('Access-Control-Allow-Origin')
    assert response.has_header('Access-Control-Allow-Headers')


@pytest.mark.django_db
def test_landing(client):
    response = client.get(reverse('name_landing'))
    assert 200 == response.status_code


@pytest.mark.xfail
def test_name_json(client):
    assert False


# TODO: Use multiple name fixtures because an empty search
# query will result in all names being returned
@pytest.mark.xfail
@pytest.mark.django_db
def test_search_with_q(client, name_fixture):
    url = reverse('name_search') + "?q={}".format(name_fixture.name)
    response = client.get(url)
    assert name_fixture.name in response.content


@pytest.mark.xfail
def test_search_with_q_type(client, name_fixture):
    assert False


@pytest.mark.xfail
def test_search_without_query(client):
    assert False
