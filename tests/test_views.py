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
    pass


@pytest.mark.xfail
def test_merged_entry_detail_returns_gone(client):
    pass


@pytest.mark.xfail
def test_merged_entry_detail_returns_ok(client):
    pass


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


@pytest.mark.xfail
def test_export(client):
    pass


@pytest.mark.xfail
def test_opensearch(client):
    pass


@pytest.mark.xfail
def test_about(client):
    pass


@pytest.mark.xfail
def test_stats(client):
    pass


@pytest.mark.xfail
def test_get_names(client):
    pass


@pytest.mark.xfail
def test_landing(client):
    pass


@pytest.mark.xfail
def test_search(client):
    pass


@pytest.mark.xfail
def test_name_json(client):
    pass
