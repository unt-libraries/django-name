from mock import MagicMock
from name.context_processors import baseurl


# rf is a pytest-django fixture
def test_baseurl_is_https(rf):
    request = rf.get('/')
    request.is_secure = MagicMock(name='is_secure', return_value=True)
    context = baseurl(request)
    assert 'https://' in context['BASE_URL']


def test_baseurl_is_http(rf):
    request = rf.get('/')
    request.is_secure = MagicMock(name='is_secure', return_value=False)
    context = baseurl(request)
    assert 'http://' in context['BASE_URL']
