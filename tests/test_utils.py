import pytest
from django.test.client import RequestFactory
from name import models, views


@pytest.fixture
def search_names(db, scope='module'):
    for x in range(1, 5):
        models.Name.objects.create(
            name="Personal {}".format(x), name_type=0)
        models.Name.objects.create(
            name="Organization {}".format(x), name_type=1)
        models.Name.objects.create(
            name="Event {}".format(x), name_type=2)
        models.Name.objects.create(
            name="Software {}".format(x), name_type=3)
        models.Name.objects.create(
            name="Building {}".format(x), name_type=4)
    return models.Name.objects.all()


# TODO: Find out if this is suppose to return the same id
#       consecutively.
@pytest.mark.xfail
def test_get_unique_user_id():
    uids = [eval(views.get_unique_user_id()) for i in range(1000)]
    assert len(uids) == len(set(uids))


@pytest.mark.django_db
def test_filter_names_with_empty_query(search_names):
    names = views.filter_names('', None)
    assert names.count() == search_names.count()


@pytest.mark.django_db
def test_filter_names_with_query(search_names):
    names = views.filter_names('1', None)
    assert names.count() == 5


@pytest.mark.django_db
@pytest.mark.parametrize('types,expected', [
    ([0], 1),
    ([0, 1], 2),
    ([0, 1, 2], 3),
    ([0, 1, 2, 3, 4], 5)
])
def test_filter_names_with_query_and_name_types(types, expected, search_names):
    names = views.filter_names('1', types)
    assert names.count() == expected


@pytest.mark.django_db
@pytest.mark.parametrize('types,expected', [
    ([0], 4),
    ([0, 1], 8),
    ([0, 1, 2], 12),
    ([0, 1, 2, 3, 4], 20)
])
def test_filter_names_with_no_query_and_name_types(types,
                                                   expected, search_names):
    names = views.filter_names('', types)
    assert names.count() == expected


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
    types = views.resolve_type(request)
    assert len(types) == expected


def test_resolve_q_returns_value():
    rf = RequestFactory()
    q = views.resolve_q(rf.get('/', {'q': 'value'}))
    assert q == 'value'


def test_resolve_q_returns_empty_string():
    rf = RequestFactory()
    q = views.resolve_q(rf.get('/'))
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
    normalized = views.normalize_query(query)
    assert len(normalized) == expected


@pytest.mark.xfail
def test_calc_total_by_month():
    assert False


@pytest.mark.xfail
def test_prepare_graph_date_range():
    assert False
