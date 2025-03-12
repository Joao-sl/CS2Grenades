from django import template

register = template.Library()


@register.filter
def split(value, delimiter=','):
    """
    split a string and return first part
    """
    if delimiter in value:
        return value.split(delimiter)[0]
    return value
