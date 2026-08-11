from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Return dictionary item for given key"""
    return dictionary.get(key)
