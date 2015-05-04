import pytest
from name import views


@pytest.mark.django_db
def test_filter_names_with_empty_query(rf, search_fixtures):
    request = rf.get('/')
    names = views.filter_names(request)
    assert names.count() == search_fixtures.count()


@pytest.mark.django_db
def test_filter_names_with_query(rf, search_fixtures):
    request = rf.get('/', {'q': 1})
    names = views.filter_names(request)
    assert names.count() == 5


@pytest.mark.django_db
@pytest.mark.parametrize('q_type,expected', [
    ('Personal', 1),
    ('Personal,Organization', 2),
    ('Personal,Organization,Event', 3),
    ('Personal,Organization,Event,Software,Building', 5)
])
def test_filter_names_with_query_and_name_types(rf, q_type,
                                                expected, search_fixtures):
    request = rf.get('/', {'q': '1', 'q_type': q_type})
    names = views.filter_names(request)
    assert names.count() == expected


@pytest.mark.django_db
@pytest.mark.parametrize('q_type,expected', [
    ('Personal', 4),
    ('Personal,Organization', 8),
    ('Personal,Organization,Event', 12),
    ('Personal,Organization,Event,Software,Building', 20)
])
def test_filter_names_with_no_query_and_name_types(rf, q_type,
                                                   expected, search_fixtures):
    request = rf.get('/', {'q_type': q_type})
    names = views.filter_names(request)
    assert names.count() == expected


# rf is a pytest-django fixture
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
def test_resolve_type(rf, query, expected):
    types = views.resolve_type(query)
    assert len(types) == expected


def test_compose_query_with_single_term():
    result = views.compose_query('testname')
    assert u'AND' in result.connector
    assert 'testname' in result.children[0]


def test_compose_query_with_multiple_terms():
    result = views.compose_query('foo bar baz bub')
    assert u'AND' in result.connector
    assert len(result.children) is 4


@pytest.mark.parametrize('query,expected', [
    ('one two three four', 4),
    ('extra   spaces      Here', 3),
    ('\try escape sequence', 3),
    ('"Pun. cua," tion! !!', 3),
])
def test_normalize_query(query, expected):
    normalized = views.normalize_query(query)
    assert len(normalized) == expected
