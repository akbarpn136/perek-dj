from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import logout
# from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Kategori, Kegiatan


# Create your views here.
def bantu_kegiatan(request):
    data_raw = [{'title': o.nama, 'description': o.referensi, 'slug': o.slug} for o in Kegiatan.objects.all()]

    return JsonResponse(data_raw, safe=False)


def index(request):
    data_kegiatan = Kegiatan.objects.all()

    data = {
        'kegiatan': data_kegiatan
    }

    return render(request, 'utama/halaman_utama.html', data)


def kegiatan_berdasarkan_kategori(request, slug, pk):
    kegiatan_kategori = Kegiatan.objects.filter(kategori_kegiatan__slug=slug, kategori_kegiatan__pk=pk)

    data = {
        'kegiatan': kegiatan_kategori
    }

    return render(request, 'utama/halaman_utama.html', data)


def cari_kegiatan(request, slug):
    teks = slug.replace('-', ' ')
    temu_kegiatan = Kegiatan.objects.filter(nama__contains=teks)

    data = {
        'kegiatan': temu_kegiatan
    }

    return render(request, 'utama/halaman_utama.html', data)


def lihat_kategori(request):
    data_kategori = Kategori.objects.all()
    paginator = Paginator(data_kategori, 50, 1)
    page = request.GET.get('halaman')

    try:
        kategori = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        kategori = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        kategori = paginator.page(paginator.num_pages)

    maks = len(paginator.page_range)

    start_number = kategori.number - 3 if kategori.number >= 4 else 0
    end_number = kategori.number + 2 if kategori.number <= maks else maks
    page_range = paginator.page_range[start_number:end_number]

    data = {
        'kategori': kategori,
        'page_range': page_range,
    }
    return render(request, 'utama/halaman_kategori.html', data)


def keluar(request):
    messages.info(request, 'Berhasil logout.')
    logout(request)

    return redirect('halaman_utama')
