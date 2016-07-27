from django import template
from django.shortcuts import get_object_or_404, Http404

from utama.models import Personil


register = template.Library()


@register.filter(name='ambil_peran_tertentu')
def ambil_peran_tertentu(value, args=None):
    try:
        data_peran = get_object_or_404(Personil, orang=value)

    except Http404:
        data_peran = Personil()

    w = data_peran.wbs_wp_pilihan
    w_nama = data_peran.wbs_wp_nama
    wbs_wp = data_peran.wbs_wp_kode
    peran = data_peran.peran
    kode = data_peran.peran_kode

    if args is None:
        return peran

    elif args is None or args == 'short':
        return peran + ' ' + wbs_wp + '.' + kode if kode != '' else peran + ' ' + wbs_wp

    elif args == 'long':
        if peran == 'TS':
            peran = 'Technical Staff'
            return peran + ' ' + wbs_wp + '.' + kode if kode != '' else peran + ' ' + wbs_wp

        elif peran == 'ES':
            peran = 'Engineering Staff'
            return peran + ' ' + wbs_wp + '.' + kode if kode != '' else peran + ' ' + wbs_wp

        elif peran == 'L':
            peran = 'Leader'
            return peran + ' ' + wbs_wp + '.' + kode if kode != '' else peran + ' ' + wbs_wp

        elif peran == 'GL':
            peran = 'Group Leader'
            return peran + ' ' + wbs_wp + '.' + kode if kode != '' else peran + ' ' + wbs_wp

        elif peran == 'CE':
            peran = 'Chief Engineering'
            return peran + ' ' + wbs_wp + '.' + kode if kode != '' else peran + ' ' + wbs_wp

        elif peran == 'ACE':
            peran = 'Assistant Chief Engineering'
            return peran + ' ' + wbs_wp + '.' + kode if kode != '' else peran + ' ' + wbs_wp

        elif peran == 'PM':
            peran = 'Program Manager'
            return peran + ' ' + wbs_wp + '.' + kode if kode != '' else peran + ' ' + wbs_wp

        elif peran == 'PD':
            peran = 'Program Director'
            return peran + ' ' + wbs_wp + '.' + kode if kode != '' else peran + ' ' + wbs_wp

    elif args == 'wbs_wp':
        return w

    elif args == 'wbs_wp_nama':
        return w_nama
