import pytest
from django.core.urlresolvers import reverse
from django.template import Template, RequestContext, Context


@pytest.mark.parametrize('url_name,arg', [
    ("name_label", "test-label"),
    ("name_json", "nm000002"),
    ("name_mads_serialize", "nm000002"),
    ("name_entry_detail", "nm000002"),
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
    'name_stats',
    'name_feed',
    'name_map',
    'name_landing',
    'name_export',
    'name_search',
    'name_names',
    'name_about',
    'name_opensearch',
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
        Template(template.format(name="name_landing"))
        .render(context)
    )

    expected = request.build_absolute_uri(reverse("name_landing"))
    assert expected, rendered


def test_get_value():
    value = 'foo'
    context = Context({'context_var': (1, value)})
    template = '{% load name_extras %}{{ context_var|get_value:1 }}'

    rendered = Template(template).render(context)
    assert value, rendered
