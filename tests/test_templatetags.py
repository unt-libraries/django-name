import pytest
from django.urls import reverse
from django.template import Template, RequestContext


@pytest.mark.parametrize('url_name,arg', [
    ("name:label", "test-label"),
    ("name:detail-json", "nm000002"),
    ("name:mads-serialize", "nm000002"),
    ("name:detail", "nm000002"),
])
def test_absolute_url_with_argument(rf, url_name, arg):
    request = rf.get("/")
    context = RequestContext(request)
    template = '{{% load name_extras %}}{{% absolute_url "{name}" "{arg}" %}}'

    rendered = (
        Template(template.format(name=url_name, arg=arg))
        .render(context)
    )

    expected = request.build_absolute_uri(reverse(url_name, args=[arg]))
    assert expected, rendered


@pytest.mark.parametrize('url_name', [
    'name:stats',
    'name:feed',
    'name:map',
    'name:landing',
    'name:export',
    'name:search',
    'name:search-json',
    'name:about',
    'name:opensearch',
])
def test_absolute_url_without_argument(rf, url_name):
    request = rf.get("/")
    context = RequestContext(request)
    template = '{{% load name_extras %}}{{% absolute_url "{name}" %}}'

    rendered = (
        Template(template.format(name=url_name))
        .render(context)
    )

    expected = request.build_absolute_uri(reverse(url_name))
    assert expected, rendered


def test_absolute_url_handles_empty_arguments(rf):
    request = rf.get("/")
    context = RequestContext(request)
    template = '{{% load name_extras %}}{{% absolute_url "{name}" "" "" %}}'

    rendered = (
        Template(template.format(name="name:landing"))
        .render(context)
    )

    expected = request.build_absolute_uri(reverse("name:landing"))
    assert expected, rendered
