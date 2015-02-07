from django import template

register = template.Library()


@register.filter
def get_value(toople, key):
    return toople[key]
