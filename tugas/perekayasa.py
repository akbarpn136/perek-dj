from django.shortcuts import get_object_or_404, Http404
from django.http import JsonResponse
from django.contrib.auth.models import User

from butir.models import ButirPerekayasa
from utama.models import Personil
from utiliti.models import Profil


def cek_keanggotaan(user, pk_kegiatan):
    anggota_kegiatan = User.objects.filter(personil__personil_kegiatan=pk_kegiatan)
    return user.pk in anggota_kegiatan.values_list('pk', flat=True)


def bantu_peran(user, hasil):
    try:
        peran = user.personil_set.values_list('peran', flat=True)[0]
    except IndexError:
        peran = ''

    if peran == 'ES':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A',
                                                    hasil__contains=hasil,
                                                    pelaksana__in=['Pertama', 'Pertama/Muda', 'Muda'])
    elif peran == 'L':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A',
                                                    hasil__contains=hasil,
                                                    pelaksana__in=['Pertama', 'Pertama/Muda', 'Muda', 'Madya'])
    elif peran == 'GL':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A',
                                                    hasil__contains=hasil,
                                                    pelaksana__in=['Muda', 'Muda/Madya', 'Madya', 'Utama'])
    elif peran == 'PM':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A',
                                                    hasil__contains=hasil,
                                                    pelaksana__in=['Muda', 'Muda/Madya', 'Madya', 'Utama'])
    elif peran == 'CE':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A',
                                                    hasil__contains=hasil,
                                                    pelaksana__in=['Madya', 'Madya/Utama', 'Utama'])
    elif peran == 'PD':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A',
                                                    hasil__contains=hasil,
                                                    pelaksana__in=['Madya', 'Madya/Utama', 'Utama'])
    else:
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='III.A')

    return data_butir


def bantu_butir_perekayasa(request, cond, keg, json=None):
    try:
        data_peran = get_object_or_404(Personil, orang=request.user, personil_kegiatan=keg, peran_utama=True)
        peran = data_peran.peran
    except Http404:
        peran = ''

    try:
        data_jenjang = get_object_or_404(Profil, user=request.user)
        jenjang = data_jenjang.jenjang
    except Http404:
        jenjang = ''

    if peran == 'ES':
        if jenjang == 'Pertama':
            faktor = 1
        elif jenjang == 'Muda':
            faktor = 1
        elif jenjang == 'Madya':
            faktor = 0
        elif jenjang == 'Utama':
            faktor = 0
        else:
            faktor = 0

    elif peran == 'L':
        if jenjang == 'Pertama':
            faktor = 0.8
        elif jenjang == 'Muda':
            faktor = 1
        elif jenjang == 'Madya':
            faktor = 1
        elif jenjang == 'Utama':
            faktor = 0
        else:
            faktor = 0

    elif peran == 'GL':
        if jenjang == 'Pertama':
            faktor = 0
        elif jenjang == 'Muda':
            faktor = 0.8
        elif jenjang == 'Madya':
            faktor = 1
        elif jenjang == 'Utama':
            faktor = 1
        else:
            faktor = 0

    elif peran == 'PM':
        if jenjang == 'Pertama':
            faktor = 0
        elif jenjang == 'Muda':
            faktor = 0.8
        elif jenjang == 'Madya':
            faktor = 1
        elif jenjang == 'Utama':
            faktor = 1
        else:
            faktor = 0

    elif peran == 'CE':
        if jenjang == 'Pertama':
            faktor = 0
        elif jenjang == 'Muda':
            faktor = 0
        elif jenjang == 'Madya':
            faktor = 0.8
        elif jenjang == 'Utama':
            faktor = 1
        else:
            faktor = 0

    elif peran == 'PD':
        if jenjang == 'Pertama':
            faktor = 0
        elif jenjang == 'Muda':
            faktor = 0
        elif jenjang == 'Madya':
            faktor = 0.8
        elif jenjang == 'Utama':
            faktor = 1
        else:
            faktor = 0
    else:
        faktor = 0

    try:
        data_butir = get_object_or_404(ButirPerekayasa, kodebutir=cond)
    except Http404:
        data_butir = ButirPerekayasa()

    data_raw = {
        'butir': data_butir.butir,
        'kodebutir': data_butir.kodebutir,
        'hasil': data_butir.hasil,
        'persentase': faktor * 100,
        'angka_asli': data_butir.angka,
        'angka': round(faktor * data_butir.angka, 3),
        'pelaksana': data_butir.pelaksana,
        'peran': peran,
        'jenjang': jenjang,
    }

    if json is None:
        return JsonResponse(data_raw, safe=False)
    else:
        return faktor * data_butir.angka
