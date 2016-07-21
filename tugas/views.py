from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import LembarInstruksi, LembarKerja


# Create your views here.
def cek_keanggotaan(user, pk_kegiatan):
    anggota_kegiatan = User.objects.filter(personil__personil_kegiatan=pk_kegiatan)
    return user.pk in anggota_kegiatan.values_list('pk', flat=True)


@login_required
def index(request, pk):
    if cek_keanggotaan(request.user, pk) or request.user.is_superuser:
        data_li = LembarInstruksi.objects.filter(kegiatan=pk)
        data_lk = LembarKerja.objects.filter(kegiatan=pk)

        data = {
            'instruksi': data_li[:9],
            'kerja': data_lk,
            'pk': pk,
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
        'keg': keg,
    }

    return render(request, 'tugas/halaman_tugas_anggota_rinci.html', data)
