from django.shortcuts import render, get_object_or_404, Http404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import LembarKeputusan
from utama.models import Kegiatan


# Create your views here.
def cek_keanggotaan(user, pk_kegiatan):
    anggota_kegiatan = User.objects.filter(personil__personil_kegiatan=pk_kegiatan)
    return user.pk in anggota_kegiatan.values_list('pk', flat=True)


def lihat_keputusan(request, slug, keg):
    if cek_keanggotaan(request.user, keg):
        if slug is None:
            pass

        try:
            kegiatan = get_object_or_404(Kegiatan, pk=keg)

        except Http404:
            messages.warning(request, 'Halaman yang dicari tidak ditemukan!')
            return redirect('halaman_utama')

        data_keputusan = LembarKeputusan.objects.filter(kegiatan=kegiatan)

        paginator = Paginator(data_keputusan.order_by('-tanggal'), 12, 1)
        page = request.GET.get('halaman')

        try:
            kep = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            kep = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            kep = paginator.page(paginator.num_pages)

        maks = len(paginator.page_range)

        start_number = kep.number - 3 if kep.number >= 4 else 0
        end_number = kep.number + 2 if kep.number <= maks else maks
        page_range = paginator.page_range[start_number:end_number]

        data = {
            'pk': kegiatan.pk,
            'kegiatan': kegiatan,
            'page_range': page_range,
            'keputusan': kep,
        }

        return render(request, 'keputusan/halaman_keputusan.html', data)

    else:
        messages.warning(request, 'Maaf, Anda tidak memiliki hak keanggotaan dari kegiatan ini.')
        return redirect('halaman_utama')
