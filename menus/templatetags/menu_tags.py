from django import template
from menus.models import Menu, Footer

register = template.Library()

@register.simple_tag()
def get_menu(slug):
    try:
        return Menu.objects.get(slug=slug)
    except Menu.DoesNotExist:
        return None
    
    
    
@register.simple_tag()
def get_footer():
    # This will fetch the first (and likely only) Footer object
    return Footer.objects.first()