from django import template

from utama.models import Kategori


register = template.Library()


@register.filter(name='ambil_kategori_tertentu')
def ambil_kategori_tertentu(value):
    data_kategori = Kategori.objects.filter(kegiatan__pk=value)
    return data_kategori
