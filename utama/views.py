from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.text import slugify

from .models import Kategori, Kegiatan
from .forms import FormKategori, FormKegiatan


# Create your views here.
def bantu_kegiatan(request):
    data_raw = [{'title': o.nama, 'description': o.referensi, 'slug': o.slug} for o in Kegiatan.objects.all()]

    return JsonResponse(data_raw, safe=False)


def index(request):
    data_kegiatan = Kegiatan.objects.all()
    paginator = Paginator(data_kegiatan, 15, 1)
    page = request.GET.get('halaman')

    try:
        kegiatan = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        kegiatan = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        kegiatan = paginator.page(paginator.num_pages)

    maks = len(paginator.page_range)

    start_number = kegiatan.number - 3 if kegiatan.number >= 4 else 0
    end_number = kegiatan.number + 2 if kegiatan.number <= maks else maks
    page_range = paginator.page_range[start_number:end_number]

    data = {
        'kegiatan': kegiatan,
        'page_range': page_range,
    }

    return render(request, 'utama/halaman_utama.html', data)


@login_required
def tambah_kegiatan(request):
    if request.method == 'POST':
        slug = slugify(request.POST.get('nama'))
        a = Kegiatan(slug=slug)
        formulir = FormKegiatan(request.POST, instance=a)

        if formulir.is_valid():
            if request.user.is_authenticated():
                messages.success(request, 'Kegiatan berhasil disimpan.')
                formulir.save()

            else:
                messages.warning(request, 'Hanya admin yang boleh menambahkan kegiatan!')

            return redirect('halaman_utama')
    else:
        formulir = FormKegiatan()

    data = {
        'form_kegiatan': formulir
    }

    if request.user.is_authenticated():
        return render(request, 'utama/halaman_modif_kegiatan.html', data)
    else:
        messages.warning(request, 'Halaman khusus admin')
        return redirect('halaman_utama')


@login_required
def ubah_kegiatan(request, slug, pk):
    kegiatan_ubah = get_object_or_404(Kegiatan, pk=pk)
    if slug is None:
        pass

    if request.method == 'POST':
        slg = slugify(request.POST.get('nama'))
        kegiatan_ubah.slug = slg
        formulir = FormKegiatan(request.POST, instance=kegiatan_ubah)

        if formulir.is_valid():
            if request.user.is_authenticated():
                messages.success(request, 'Kegiatan berhasil disimpan.')
                formulir.save()

            else:
                messages.warning(request, 'Hanya admin yang boleh mengubah kegiatan!')

            return redirect('halaman_utama')
    else:
        formulir = FormKegiatan(instance=kegiatan_ubah)

    data = {
        'form_kegiatan': formulir,
    }

    if request.user.is_authenticated():
        return render(request, 'utama/halaman_modif_kegiatan.html', data)
    else:
        messages.warning(request, 'Halaman khusus admin')
        return redirect('halaman_utama')


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


@login_required
def tambah_kategori(request):
    if request.method == 'POST':
        slug = slugify(request.POST.get('nama'))
        a = Kategori(slug=slug)
        formulir = FormKategori(request.POST, instance=a)

        if formulir.is_valid():
            messages.success(request, 'Kategori berhasil disimpan.')
            formulir.save()

            return redirect('halaman_kategori')
    else:
        formulir = FormKategori()

    data = {
        'form_kategori': formulir
    }
    return render(request, 'utama/halaman_modif_kategori.html', data)


@login_required
def ubah_kategori(request, slug, pk):
    kategori_ubah = get_object_or_404(Kategori, pk=pk)
    if slug is None:
        pass

    if request.method == 'POST':
        slg = slugify(request.POST.get('nama'))
        kategori_ubah.slug = slg
        formulir = FormKategori(request.POST, instance=kategori_ubah)

        if formulir.is_valid():
            messages.success(request, 'Kategori berhasil disimpan.')
            formulir.save()

            return redirect('halaman_kategori')
    else:
        formulir = FormKategori(instance=kategori_ubah)

    data = {
        'form_kategori': formulir,
        'kategori': kategori_ubah
    }
    return render(request, 'utama/halaman_modif_kategori.html', data)


@login_required
def hapus_kategori(request, slug, pk):
    if slug is None:
        pass

    kategori_ubah = get_object_or_404(Kategori, pk=pk)

    if kategori_ubah.delete():
        messages.success(request, 'Sekali lagi, kategori berhasil dihapus.')
        html = '''<div class="ui green message">
            <div class="header">
                Info
            </div>
            <p>
                Kategori berhasil dihapus.
            </p>
        </div>'''
        return HttpResponse(html)


def keluar(request):
    messages.info(request, 'Berhasil logout.')
    logout(request)

    return redirect('halaman_utama')
