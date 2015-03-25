import pytest
from .test_views import twenty_name_fixtures
from django.test.client import RequestFactory
from name.views import (
    normalize_query,
    resolve_q,
    resolve_type,
    filter_names
)

# FIXME: This is used to silence PEP8 warnings
twenty_name_fixtures = twenty_name_fixtures


@pytest.mark.xfail
def test_get_unique_user_id():
    assert False


@pytest.mark.django_db
def test_filter_names_with_empty_query(twenty_name_fixtures):
    names = filter_names('', None)
    assert names.count() == twenty_name_fixtures.count()


# TODO: Create a new fixture where we know how many of
#       each type is known
@pytest.mark.django_db
def test_filter_names_with_query(twenty_name_fixtures):
    names = filter_names('1', None)
    assert names.count() == 11


@pytest.mark.parametrize('query,expected', [
    ('Personal', 1),
    ('Personal,Building,Organization', 3),
    ('Personal,Building,Organization,Software,Event', 5),
    ('Personal,Building,Organization,', 3),
    ('Personal, Location, Organiztion', 1),
    ('Personal, Building, Organiztion,', 1),
    ('Personal Building Organiztion', 0),
    ('Unknown,Types', 0),
    ('Unknown,Types', 0)
])
def test_resolve_type(query, expected):
    rf = RequestFactory()
    request = rf.get('/', {'q_type': query})
    types = resolve_type(request)
    assert len(types) == expected


def test_resolve_q_returns_value():
    rf = RequestFactory()
    q = resolve_q(rf.get('/', {'q': 'value'}))
    assert q == 'value'


def test_resolve_q_returns_empty_string():
    rf = RequestFactory()
    q = resolve_q(rf.get('/'))
    assert '' == q


@pytest.mark.xfail
def test_get_query():
    assert False


@pytest.mark.parametrize('query,expected', [
    ('one two three four', 4),
    ('extra   spaces      Here', 3),
    ('\try escape sequence', 3),
    ('"Pun. cua," tion! !!', 3),
])
def test_normalize_query(query, expected):
    normalized = normalize_query(query)
    assert len(normalized) == expected


@pytest.mark.xfail
def test_calc_total_by_month():
    assert False


@pytest.mark.xfail
def test_prepare_graph_date_range():
    assert False
