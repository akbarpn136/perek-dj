from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.text import slugify

from .models import Kategori, Kegiatan, Format, Personil
from .forms import FormKategori, FormKegiatan, FormFormat, FormPersonil, FormMasuk


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
            if request.user.is_superuser:
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

    if request.user.is_superuser:
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
            if request.user.is_superuser:
                messages.success(request, 'Kegiatan berhasil disimpan.')
                formulir.save()

            else:
                messages.warning(request, 'Hanya admin yang boleh mengubah kegiatan!')

            return redirect('halaman_utama')
    else:
        formulir = FormKegiatan(instance=kegiatan_ubah)

    data = {
        'form_kegiatan': formulir,
        'kegiatan': kegiatan_ubah
    }

    if request.user.is_superuser:
        return render(request, 'utama/halaman_modif_kegiatan.html', data)
    else:
        messages.warning(request, 'Halaman khusus admin')
        return redirect('halaman_utama')


@login_required
def hapus_kegiatan(request, slug, pk):
    if slug is None:
        pass

    kegiatan_ubah = get_object_or_404(Kegiatan, pk=pk)

    if request.user.is_superuser:
        if kegiatan_ubah.delete():
            html = '''<div class="ui green message">
                <div class="header">
                    Info
                </div>
                <p>
                    Kegiatan berhasil dihapus.
                </p>
            </div>'''
            return HttpResponse(html)
    else:
        html = '''<div class="ui red message">
            <div class="header">
                Info
            </div>
            <p>
                Kegiatan hanya boleh dihapus oleh admin.
            </p>
        </div>'''
        return HttpResponse(html)


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


def user_kegiatan(request):
    data_keg_user = Kegiatan.objects.filter(personil__orang__pk=request.user.pk)

    data = {
        'kegiatan': data_keg_user
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
        html = '''<div class="ui green message">
            <div class="header">
                Info
            </div>
            <p>
                Kategori berhasil dihapus.
            </p>
        </div>'''
        return HttpResponse(html)


@login_required
def lihat_format(request, pk):
    data_format = Format.objects.all()
    data_keg = get_object_or_404(Kegiatan, pk=pk)

    data = {
        'format': data_format,
        'keg': data_keg
    }

    return render(request, 'utama/halaman_format.html', data)


@login_required
def tambah_format(request, pk):
    kegiatan = get_object_or_404(Kegiatan, pk=pk)
    if request.method == 'POST':
        a = Format(format_kegiatan=kegiatan)
        formulir = FormFormat(request.POST, instance=a)

        if formulir.is_valid():
            if request.user.is_superuser:
                messages.success(request, 'Format berhasil disimpan.')
                formulir.save()

            else:
                messages.warning(request, 'hanya dapat dilakukan oleh admin.')

            return redirect('halaman_format', pk=pk)
    else:
        formulir = FormFormat()

    data = {
        'form_format': formulir,
        'index': kegiatan
    }

    if request.user.is_superuser:
        return render(request, 'utama/halaman_modif_format.html', data)

    else:
        messages.warning(request, 'hanya dapat dilakukan oleh admin.')
        return redirect('halaman_format', pk=pk)


@login_required
def ubah_format(request, pk, keg_id):
    frmt = get_object_or_404(Format, pk=pk)
    kegiatan = get_object_or_404(Kegiatan, pk=keg_id)

    if request.method == 'POST':
        formulir = FormFormat(request.POST, instance=frmt)

        if formulir.is_valid():
            if request.user.is_superuser:
                messages.success(request, 'Format berhasil disimpan.')
                formulir.save()

            else:
                messages.warning(request, 'hanya dapat dilakukan oleh admin.')

            return redirect('halaman_format', pk=keg_id)
    else:
        formulir = FormFormat(instance=frmt)

    data = {
        'form_format': formulir,
        'index': kegiatan,
        'format': frmt
    }

    if request.user.is_superuser:
        return render(request, 'utama/halaman_modif_format.html', data)

    else:
        messages.warning(request, 'hanya dapat dilakukan oleh admin.')
        return redirect('halaman_format', pk=keg_id)


@login_required
def hapus_format(request, pk):
    format_ubah = get_object_or_404(Format, pk=pk)

    if request.user.is_superuser:
        if format_ubah.delete():
            html = '''<div class="ui green message">
                <div class="header">
                    Info
                </div>
                <p>
                    Format berhasil dihapus.
                </p>
            </div>'''
            return HttpResponse(html)
    else:
        html = '''<div class="ui red message">
            <div class="header">
                Info
            </div>
            <p>
                Format hanya boleh dihapus oleh admin.
            </p>
        </div>'''
        return HttpResponse(html)


def lihat_personil(request, pk):
    data_personil = Personil.objects.filter(personil_kegiatan=pk)
    kegiatan_tertentu = get_object_or_404(Kegiatan, pk=pk)

    data = {
        'personil': data_personil,
        'kegiatan': kegiatan_tertentu,
    }

    return render(request, 'utama/halaman_personil.html', data)


@login_required
def tambah_personil(request, pk):
    kegiatan_tertentu = get_object_or_404(Kegiatan, pk=pk)

    if request.method == 'POST':
        a = Personil(personil_kegiatan=kegiatan_tertentu)
        formulir = FormPersonil(request.POST, instance=a)

        if formulir.is_valid():
            if request.user.is_superuser:
                messages.success(request, 'Data personil berhasil disimpan')
                formulir.save()

            else:
                messages.warning(request, 'Simpan data personil hanya dapat dilakukan oleh admin.')
            return redirect('halaman_personil', pk=kegiatan_tertentu.pk)
    else:
        formulir = FormPersonil()

    data = {
        'formulir': formulir,
        'kegiatan': kegiatan_tertentu
    }

    if request.user.is_superuser:
        return render(request, 'utama/halaman_modif_personil.html', data)
    else:
        messages.warning(request, 'Hanya dapat dilakukan oleh admin.')
        return redirect('halaman_utama')


@login_required
def ubah_personil(request, pk, pk_personil):
    kegiatan_tertentu = get_object_or_404(Kegiatan, pk=pk)
    personil_tertentu = get_object_or_404(Personil, pk=pk_personil)

    if request.method == 'POST':
        formulir = FormPersonil(request.POST, instance=personil_tertentu)

        if formulir.is_valid():
            if request.user.is_superuser:
                messages.success(request, 'Data personil berhasil disimpan')
                formulir.save()

            else:
                messages.warning(request, 'Simpan data personil hanya dapat dilakukan oleh admin.')
            return redirect('halaman_personil', pk=kegiatan_tertentu.pk)
    else:
        formulir = FormPersonil(instance=personil_tertentu)

    data = {
        'formulir': formulir,
        'kegiatan': kegiatan_tertentu,
        'personil': personil_tertentu
    }

    if request.user.is_superuser:
        return render(request, 'utama/halaman_modif_personil.html', data)
    else:
        messages.warning(request, 'Hanya dapat dilakukan oleh admin.')
        return redirect('halaman_utama')


@login_required
def hapus_personil(request, pk):
    personil_ubah = get_object_or_404(Personil, pk=pk)

    if request.user.is_superuser:
        if personil_ubah.delete():
            html = '''<div class="ui green message">
                    <div class="header">
                        Info
                    </div>
                    <p>
                        Personil berhasil dihapus.
                    </p>
                </div>'''
            return HttpResponse(html)
    else:
        html = '''<div class="ui red message">
                <div class="header">
                    Info
                </div>
                <p>
                    Personil hanya boleh dihapus oleh admin.
                </p>
            </div>'''
        return HttpResponse(html)


def masuk(request):
    if request.user.is_authenticated():
        messages.warning(request, 'Sudah terotentikasi...')
        return redirect('halaman_utama')
    else:
        if request.method == 'POST':
            a = request.POST.get('username')
            b = request.POST.get('password')
            lanjut = request.GET.get('next')

            formulir = FormMasuk(request.POST)
            if formulir.is_valid():
                user = authenticate(username=a, password=b)

                if user is None:
                    messages.warning(request, 'username atau password salah.')
                    return redirect('halaman_login')
                else:
                    login(request, user)
                    messages.success(request, 'Selamat datang, ' + request.user.username)
                    if lanjut is None:
                        return redirect('halaman_utama')
                    else:
                        return redirect(lanjut)

        else:
            formulir = FormMasuk()

        data = {
            'formulir': formulir
        }
        return render(request, 'registration/halaman_masuk.html', data)


def keluar(request):
    messages.info(request, 'Berhasil logout.')
    logout(request)

    return redirect('halaman_utama')
