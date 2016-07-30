from django import template
from django.shortcuts import get_object_or_404, Http404

from utama.models import Personil


register = template.Library()


@register.filter(name='ambil_peran_tertentu')
def ambil_peran_tertentu(value, args=None):
    try:
        org, keg = value
    except ValueError:
        org = value
        keg = 0
    except TypeError:
        org = value
        keg = 0

    try:
        data_peran = get_object_or_404(Personil, orang=org, personil_kegiatan=keg, peran_utama=True)

    except Http404:
        data_peran = Personil()

    w = data_peran.wbs_wp_pilihan
    w_nama = data_peran.wbs_wp_nama
    wbs_wp = data_peran.wbs_wp_kode
    peran = data_peran.peran
    kode = data_peran.peran_kode

    if args is None:
        return None

    elif args == 'singkatan':
        return peran

    elif args == 'short':
        if wbs_wp == '0' and kode == '0':
            return peran

        else:
            return peran + ' ' + wbs_wp + '.' + kode if kode != '' else peran + ' ' + wbs_wp

    elif args == 'long':
        if peran == 'TS':
            peran = 'Technical Staff'
            if wbs_wp == '0' and kode == '0':
                return peran

            else:
                return peran + ' ' + wbs_wp + '.' + kode if kode != '' else peran + ' ' + wbs_wp

        elif peran == 'ES':
            peran = 'Engineering Staff'
            if wbs_wp == '0' and kode == '0':
                return peran

            else:
                return peran + ' ' + wbs_wp + '.' + kode if kode != '' else peran + ' ' + wbs_wp

        elif peran == 'L':
            peran = 'Leader'
            if wbs_wp == '0' and kode == '0':
                return peran

            else:
                return peran + ' ' + wbs_wp + '.' + kode if kode != '' else peran + ' ' + wbs_wp

        elif peran == 'GL':
            peran = 'Group Leader'
            if wbs_wp == '0' and kode == '0':
                return peran

            else:
                return peran + ' ' + wbs_wp + '.' + kode if kode != '' else peran + ' ' + wbs_wp

        elif peran == 'CE':
            peran = 'Chief Engineering'
            if wbs_wp == '0' and kode == '0':
                return peran

            else:
                return peran + ' ' + wbs_wp + '.' + kode if kode != '' else peran + ' ' + wbs_wp

        elif peran == 'ACE':
            peran = 'Assistant Chief Engineering'
            if wbs_wp == '0' and kode == '0':
                return peran

            else:
                return peran + ' ' + wbs_wp + '.' + kode if kode != '' else peran + ' ' + wbs_wp

        elif peran == 'PM':
            peran = 'Program Manager'
            if wbs_wp == '0' and kode == '0':
                return peran

            else:
                return peran + ' ' + wbs_wp + '.' + kode if kode != '' else peran + ' ' + wbs_wp

        elif peran == 'PD':
            peran = 'Program Director'
            if wbs_wp == '0' and kode == '0':
                return peran

            else:
                return peran + ' ' + wbs_wp + '.' + kode if kode != '' else peran + ' ' + wbs_wp

    elif args == 'wbs_wp':
        return w

    elif args == 'wbs_wp_nama':
        return w_nama
