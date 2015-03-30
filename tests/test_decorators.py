from name.decorators import jsonp
from mock import MagicMock


def test_jsonp_returns_without_status_code_200():
    # Setup the mock view.
    f = MagicMock()
    f.__name__ = 'Wrapped View'

    # Setup the mock response.
    response = MagicMock()
    response.status_code = 301

    # Set the response as the return value for the mock
    # view.
    f.return_value = response

    decorated_f = jsonp(f)
    assert decorated_f(1)


def test_jsonp_returns_has_callback():
    f = MagicMock()
    f.__name__ = 'Wrapped View'

    # Setup the mock request
    request = MagicMock()
    request.GET = dict(callback='init')

    # Setup the mock response.
    json = {"id": 1, "status": 200}
    response = MagicMock(content=json, status_code=200)

    f.return_value = response
    decorated_f = jsonp(f)

    result = decorated_f(request)

    expected = 'init({0})'.format(json)
    assert expected == result.content


def test_jsonp_request_does_not_have_callback():
    f = MagicMock()
    f.__name__ = 'Wrapped View'

    request = MagicMock()
    request.GET = dict()

    json = {"id": 1, "status": 200}
    response = MagicMock(content=json, status_code=200)

    f.return_value = response
    decorated_f = jsonp(f)

    result = decorated_f(request)
    # Here we assert the the content was not altered
    # since we did not provide a callback.
    assert json == result.content
