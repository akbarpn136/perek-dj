from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

import hashlib

from .models import LembarInstruksi, LembarKerja


# Create your views here.
def bantu_gravatar(request, usr):
    u = get_object_or_404(User, username=usr)
    data_raw = [{
        'hash': hashlib.md5(u.email.encode()).hexdigest(),
        'full_name': u.get_full_name(),
        'username': u.username,
    }]

    return JsonResponse(data_raw, safe=False)


def cek_keanggotaan(user, pk_kegiatan):
    anggota_kegiatan = User.objects.filter(personil__personil_kegiatan=pk_kegiatan)
    return user.pk in anggota_kegiatan.values_list('pk', flat=True)


@login_required
def index(request, pk, usr=None):
    if cek_keanggotaan(request.user, pk) or request.user.is_superuser:
        if usr is None:
            data_li = LembarInstruksi.objects.filter(kegiatan=pk)
        else:
            try:
                u = get_object_or_404(User, username=usr)
                u_value = u.pk
            except Http404:
                u_value = 0

            data_li = LembarInstruksi.objects.filter(kegiatan=pk, penerima=u_value)

        data_lk = LembarKerja.objects.filter(kegiatan=pk)

        paginator = Paginator(data_li, 12, 1)
        page = request.GET.get('halaman')

        try:
            li = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            li = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            li = paginator.page(paginator.num_pages)

        maks = len(paginator.page_range)

        start_number = li.number - 3 if li.number >= 4 else 0
        end_number = li.number + 2 if li.number <= maks else maks
        page_range = paginator.page_range[start_number:end_number]

        anggota_kegiatan = User.objects.filter(personil__personil_kegiatan=pk).distinct()

        data = {
            'instruksi': li,
            'kerja': data_lk,
            'pk': pk,
            'page_range': page_range,
            'personil': anggota_kegiatan,
        }

        return render(request, 'tugas/halaman_tugas_anggota.html', data)
    else:
        messages.warning(request, 'Maaf, Anda tidak memiliki hak keanggotaan dari kegiatan ini.')
        return redirect('halaman_utama')


@login_required
def lihat_li(request, slug, pk, keg):
    if slug is None:
        pass

    data_lk = LembarKerja.objects.filter(li=pk)
    data_li_semua = LembarInstruksi.objects.filter(kegiatan=keg)

    try:
        data_li = get_object_or_404(LembarInstruksi, pk=pk)
    except Http404:
        messages.warning(request, 'Lembar instruksi tidak ditemukan!')
        return redirect('halaman_tugas_anggota', pk=keg)

    data = {
        'instruksi': data_li_semua,
        'kerja': data_lk,
        'li': data_li,
        'pk': keg,
    }

    return render(request, 'tugas/halaman_tugas_anggota_rinci.html', data)
