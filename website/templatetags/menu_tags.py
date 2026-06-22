from django import template
from home.models import Menu

register = template.Library()


@register.simple_tag
def get_menu(title):
    """
    Usage: {% get_menu "Main Menu" as main_menu %}
    """
    try:
        return Menu.objects.prefetch_related("items__children").get(title=title)
    except Menu.DoesNotExist:
        return None
