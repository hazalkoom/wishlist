from django import template
from app1.models import Wish

register = template.Library()


@register.simple_tag
def get_all_wishes():
    return Wish.objects.all()

@register.filter
def dict_get(d, key):
    return d.get(key)