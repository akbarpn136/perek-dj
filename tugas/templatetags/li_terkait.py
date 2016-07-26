from django import template
from django.shortcuts import get_object_or_404, Http404

from tugas.models import LembarInstruksi


register = template.Library()


@register.filter(name='ambil_li_tertentu')
def ambil_li_tertentu(value):
    try:
        data_li = get_object_or_404(LembarInstruksi, pk=value)

    except Http404:
        data_li = LembarInstruksi()

    return data_li.nomor
