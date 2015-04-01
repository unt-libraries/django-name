import pytest
from name import views


def test_get_unique_user_id():
    '''Test get_unique_user_id.
    
    Should always return the same ID for a single host.
    '''
    uids = [views.get_unique_user_id for i in range(1000)]
    assert 1 == len(set(uids))


@pytest.mark.django_db
def test_filter_names_with_empty_query(search_fixtures):
    names = views.filter_names('', None)
    assert names.count() == search_fixtures.count()


@pytest.mark.django_db
def test_filter_names_with_query(search_fixtures):
    names = views.filter_names('1', None)
    assert names.count() == 5


@pytest.mark.django_db
@pytest.mark.parametrize('types,expected', [
    ([0], 1),             # Personal
    ([0, 1], 2),          # Personal, Organization
    ([0, 1, 2], 3),       # Personal, Organization, Event
    ([0, 1, 2, 3, 4], 5)  # All name types.
])
def test_filter_names_with_query_and_name_types(types,
                                                expected, search_fixtures):
    names = views.filter_names('1', types)
    assert names.count() == expected


@pytest.mark.django_db
@pytest.mark.parametrize('types,expected', [
    ([0], 4),              # Personal
    ([0, 1], 8),           # Personal, Organization
    ([0, 1, 2], 12),       # Personal, Organization, Event
    ([0, 1, 2, 3, 4], 20)  # All name types.
])
def test_filter_names_with_no_query_and_name_types(types,
                                                   expected, search_fixtures):
    names = views.filter_names('', types)
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
    request = rf.get('/', {'q_type': query})
    types = views.resolve_type(request)
    assert len(types) == expected


def test_resolve_q_returns_value(rf):
    q = views.resolve_q(rf.get('/', {'q': 'value'}))
    assert q == 'value'


def test_resolve_q_returns_empty_string(rf):
    q = views.resolve_q(rf.get('/'))
    assert '' == q


@pytest.mark.xfail(reason='No Test')
def test_get_query():
    assert False


@pytest.mark.parametrize('query,expected', [
    ('one two three four', 4),
    ('extra   spaces      Here', 3),
    ('\try escape sequence', 3),
    ('"Pun. cua," tion! !!', 3),
])
def test_normalize_query(query, expected):
    normalized = views.normalize_query(query)
    assert len(normalized) == expected


@pytest.mark.xfail(reason='No Test')
def test_calc_total_by_month():
    assert False


@pytest.mark.xfail(reason='No Test')
def test_prepare_graph_date_range():
    assert False
