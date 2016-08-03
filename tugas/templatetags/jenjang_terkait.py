from django import template
from django.shortcuts import get_object_or_404, Http404

from utiliti.models import Profil


register = template.Library()


@register.filter(name='ambil_jenjang')
def ambil_jenjang(value):
    try:
        data_jenjang = get_object_or_404(Profil, user=value)
    except Http404:
        data_jenjang = Profil()

    return data_jenjang.jenjang
