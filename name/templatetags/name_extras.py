from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag(name="absolute_url", takes_context=True)
def absolute_url(context, name, *args):
    request = context.get('request')
    return request.build_absolute_uri(
        reverse(name, args=filter(None, list(args))))
