from django import template
import hashlib

register = template.Library()


@register.filter(name='hash_email')
def hash_email(value):
    return hashlib.md5(value.encode()).hexdigest()
