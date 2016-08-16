from django.shortcuts import render, redirect, get_object_or_404, Http404, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.utils.text import slugify
from django.views.decorators.cache import cache_control

import hashlib

from .models import LembarInstruksi, LembarKerja, Kegiatan, Logbook
from butir.models import ButirPerekayasa
from utama.models import Format, Personil
from utiliti.models import Profil
from .forms import FormLI, FormKesepakatan, FormLK


# Create your views here.
def bantu_gravatar(request, usr):
    u = get_object_or_404(User, username=usr)
    data_raw = [{
        'hash': hashlib.md5(u.email.encode()).hexdigest(),
        'full_name': u.get_full_name(),
        'username': u.username,
    }]

    return JsonResponse(data_raw, safe=False)


def bantu_peran(request, usr, keg):
    try:
        data_peran = get_object_or_404(Personil, orang=usr, personil_kegiatan=keg, peran_utama=True)

    except Http404:
        data_peran = Personil()

    data_raw = [{
        'peran': data_peran.peran,
        'kode': data_peran.peran_kode,
        'wbs_wp': data_peran.wbs_wp_nama,
        'wbs_wp_kode': data_peran.wbs_wp_kode,
    }]

    return JsonResponse(data_raw, safe=False)


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

        paginator = Paginator(data_li.order_by('-tanggal'), 12, 1)
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

        try:
            data_kegiatan = get_object_or_404(Kegiatan, pk=pk)
        except Http404:
            messages.warning(request, 'Kegiatan tidak ditemukan')
            data_kegiatan = Kegiatan()

        data = {
            'kode_tugas': 'IS',
            'instruksi': li,
            'kerja': data_lk,
            'pk': pk,
            'kegiatan': data_kegiatan,
            'page_range': page_range,
            'personil': anggota_kegiatan,
            'peran': [request.user.pk, data_kegiatan.pk],
        }

        return render(request, 'tugas/halaman_tugas_anggota.html', data)
    else:
        messages.warning(request, 'Maaf, Anda tidak memiliki hak keanggotaan dari kegiatan ini.')
        return redirect('halaman_utama')


@login_required
def lihat_li(request, slug, pk, keg):
    if slug is None:
        pass

    data_lk = LembarKerja.objects.filter(li=pk, kegiatan=keg)
    data_logbook = Logbook.objects.filter(kegiatan=keg)
    data_li_semua = LembarInstruksi.objects.filter(kegiatan=keg)

    try:
        data_li = get_object_or_404(LembarInstruksi, pk=pk)
    except Http404:
        messages.warning(request, 'Lembar instruksi tidak ditemukan!')
        return redirect('halaman_tugas_anggota', pk=keg)

    data = {
        'kode_tugas': 'IS',
        'instruksi': data_li_semua,
        'kerja': data_lk,
        'logbook': data_logbook,
        'lmbr': data_li,
        'pk': keg,
        'is_exist': True,
    }

    if request.user.username == data_li.pemberi.username or request.user.username == data_li.penerima.username:
        return render(request, 'tugas/halaman_li_anggota_rinci.html', data)
    else:
        messages.warning(request, 'Hanya pemberi dan penerima tugas saja yang memiliki hak akses!')
        return redirect('halaman_tugas_anggota', pk=keg)


@login_required
def lihat_li_rinci(request, slug, pk, keg):
    if slug is None:
        pass

    try:
        data_li = get_object_or_404(LembarInstruksi, pk=pk)
    except Http404:
        messages.warning(request, 'Lembar instruksi tidak ditemukan!')
        return redirect('halaman_tugas_anggota', pk=keg)

    try:
        data_keg = get_object_or_404(Kegiatan, pk=keg)
    except Http404:
        messages.warning(request, 'Kegiatan/Program tidak ditemukan!')
        return redirect('halaman_tugas_anggota', pk=keg)

    data = {
        'lmbr': data_li,
        'pk': keg,
        'kegiatan': data_keg,
        'peran': [data_li.pemberi.pk, data_keg.pk],
        'peran_penerima': [data_li.penerima.pk, data_keg.pk],
    }

    if data_li.pemberi.username == request.user.username or data_li.penerima.username == request.user.username or \
            request.user.is_superuser:
        return render(request, 'tugas/halaman_cetak_li_lembaran.html', data)
    else:
        messages.warning(request, 'Hanya pemilik yang mendapatkan hak akses!')
        # return redirect('/tugas/%s-%s-%s/rincian/' % (slugify(data_li.nomor, allow_unicode=True), pk, keg))
        return redirect('halaman_li_anggota_rinci', slug=slugify(data_li.nomor, allow_unicode=True), pk=pk, keg=keg)


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def tambah_li(request, slug, keg, kode):
    if slug is None:
        pass

    try:
        data_peran = get_object_or_404(Personil, orang=request.user, personil_kegiatan=keg, peran_utama=True)
    except Http404:
        messages.warning(request, 'Anda tidak memiliki peran dalam kegiatan ini!')
        return redirect('halaman_tugas_anggota', pk=keg)

    data_kegiatan = get_object_or_404(Kegiatan, pk=keg)
    data_li = LembarInstruksi.objects.filter(kegiatan=keg, penerima=request.user).exclude(pemberi=request.user)

    try:
        data_format = get_object_or_404(Format, format_kegiatan=keg, kode=kode)

    except Http404:
        messages.warning(request, 'Format lembar instruksi tidak ditemukan...')
        return redirect('halaman_tugas_anggota', pk=keg)

    if request.method == 'POST':
        butir = request.POST.get('butir')
        angka = request.POST.get('angka_hid')
        cek_angka = round(bantu_butir_perekayasa(request, butir, keg, 'na'), 3)

        a = LembarInstruksi(kegiatan=Kegiatan.objects.get(pk=keg), pemberi=request.user, angka=angka)

        formulir = FormLI(request.POST, instance=a)

        if formulir.is_valid():
            if cek_keanggotaan(request.user, keg):
                if float(angka) == cek_angka:
                    messages.success(request, 'Lembar instruksi berhasil ditambahkan')
                    a.save()
                else:
                    messages.warning(request, 'Tidak diperbolehkan untuk mengganti angka kredit!')
                    return redirect('halaman_tambah_li_anggota', slug=slug, keg=keg, kode=kode)

            else:
                messages.warning(request, 'Maaf, Anda tidak mendapatkan hak akses!')
                return redirect('halaman_tugas_anggota', pk=keg)

    else:
        formulir = FormLI()

    if data_peran.peran == 'GL':
        if data_peran.wbs_wp_kode == '0':
            formulir.fields['penerima'].choices = \
                [('', '-----')] + [(user.pk, '[' +
                                    user.personil_set.filter(orang=user.pk, peran_utama=True,
                                                             personil_kegiatan=keg).values_list('peran',
                                                                                                flat=True)[
                                        0] + ']' + ' ' + user.get_full_name()) for user in
                                   User.objects.filter(personil__personil_kegiatan=keg,
                                                       personil__peran__in=['L']).order_by(
                                       'username').distinct().exclude(
                                       pk=request.user.pk)]

        else:
            formulir.fields['penerima'].choices = \
                [('', '-----')] + [(user.pk, '[' +
                                    user.personil_set.filter(orang=user.pk, peran_utama=True,
                                                             personil_kegiatan=keg).values_list('peran',
                                                                                                flat=True)[
                                        0] + ']' + ' ' + user.get_full_name()) for user in
                                   User.objects.filter(personil__personil_kegiatan=keg,
                                                       personil__peran__in=['L'],
                                                       personil__wbs_wp_kode=data_peran.wbs_wp_kode).order_by(
                                       'username').distinct().exclude(
                                       pk=request.user.pk)]

    elif data_peran.peran == 'L':
        formulir.fields['penerima'].choices = \
            [('', '-----')] + [(user.pk, '[' +
                                user.personil_set.filter(orang=user.pk, peran_utama=True,
                                                         personil_kegiatan=keg).values_list('peran',
                                                                                            flat=True)[
                                    0] + ']' + ' ' + user.get_full_name()) for user in
                               User.objects.filter(personil__personil_kegiatan=keg,
                                                   personil__peran__in=['ES'],
                                                   personil__wbs_wp_kode=data_peran.wbs_wp_kode).order_by(
                                   'username').distinct().exclude(
                                   pk=request.user.pk)]

    try:
        peran = request.user.personil_set.values_list('peran', flat=True)[0]
    except IndexError:
        peran = ''

    if peran == 'ES':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A', hasil__contains='Lembar Instruksi',
                                                    pelaksana__in=['Pertama', 'Pertama/Muda', 'Muda'])
    elif peran == 'L':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A', hasil__contains='Lembar Instruksi',
                                                    pelaksana__in=['Pertama', 'Pertama/Muda', 'Muda', 'Madya'])
    elif peran == 'GL':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A', hasil__contains='Lembar Instruksi',
                                                    pelaksana__in=['Muda', 'Muda/Madya', 'Madya', 'Utama'])
    elif peran == 'PM':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A', hasil__contains='Lembar Instruksi',
                                                    pelaksana__in=['Muda', 'Muda/Madya', 'Madya', 'Utama'])
    elif peran == 'CE':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A', hasil__contains='Lembar Instruksi',
                                                    pelaksana__in=['Madya', 'Madya/Utama', 'Utama'])
    elif peran == 'PD':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A', hasil__contains='Lembar Instruksi',
                                                    pelaksana__in=['Madya', 'Madya/Utama', 'Utama'])
    else:
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='III.A')

    data = {
        'pk': keg,
        'li': data_li,
        'kegiatan': data_kegiatan,
        'peran': [request.user, keg],
        'formulir': formulir,
        'format': data_format,
        'butir': data_butir,
    }

    if data_peran.peran in ['GL', 'L']:
        return render(request, 'tugas/halaman_li_anggota_modifikasi.html', data)
    else:
        messages.warning(request, 'Hanya dapat dilakukan oleh Group Leader atau Leader')
        return redirect('halaman_tugas_anggota', pk=keg)


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ubah_li(request, slug, keg, kode, li):
    if slug is None:
        pass

    try:
        data_peran = get_object_or_404(Personil, orang=request.user, personil_kegiatan=keg, peran_utama=True)
    except Http404:
        messages.warning(request, 'Anda tidak memiliki peran dalam kegiatan ini!')
        return redirect('halaman_tugas_anggota', pk=keg)

    data_kegiatan = get_object_or_404(Kegiatan, pk=keg)
    data_li = LembarInstruksi.objects.filter(kegiatan=keg, penerima=request.user).exclude(pemberi=request.user)
    li = get_object_or_404(LembarInstruksi, pk=li)

    try:
        data_format = get_object_or_404(Format, format_kegiatan=keg, kode=kode)

    except Http404:
        messages.warning(request, 'Format lembar instruksi tidak ditemukan...')
        return redirect('halaman_tugas_anggota', pk=keg)

    if request.method == 'POST':
        butir = request.POST.get('butir')

        try:
            angka = request.POST.get('angka_hid')
        except ValueError:
            angka = 0
        except TypeError:
            angka = 0
            messages.warning(request, 'Harus dalam bentuk angka!')

        cek_angka = round(bantu_butir_perekayasa(request, butir, keg, 'na'), 3)

        li.angka = angka

        formulir = FormLI(request.POST, instance=li)

        if formulir.is_valid():
            if cek_keanggotaan(request.user, keg):
                if float(angka) == cek_angka:
                    messages.success(request, 'Lembar instruksi berhasil disimpan')
                    li.save()
                else:
                    messages.warning(request, 'Tidak diperbolehkan untuk mengganti angka kredit!')
                    # return redirect('halaman_tambah_li_anggota', slug=slug, keg=keg, kode=kode)

            else:
                messages.warning(request, 'Maaf, Anda tidak mendapatkan hak akses!')
                return redirect('halaman_tambah_li_anggota', slug=slug, keg=keg, kode=kode)

    else:
        formulir = FormLI(instance=li)

    if data_peran.peran == 'GL':
        if data_peran.wbs_wp_kode == '0':
            formulir.fields['penerima'].choices = \
                [('', '-----')] + [(user.pk, '[' +
                                    user.personil_set.filter(orang=user.pk, peran_utama=True,
                                                             personil_kegiatan=keg).values_list('peran',
                                                                                                flat=True)[
                                        0] + ']' + ' ' + user.get_full_name()) for user in
                                   User.objects.filter(personil__personil_kegiatan=keg,
                                                       personil__peran__in=['L']).order_by(
                                       'username').distinct().exclude(
                                       pk=request.user.pk)]

        else:
            formulir.fields['penerima'].choices = \
                [('', '-----')] + [(user.pk, '[' +
                                    user.personil_set.filter(orang=user.pk, peran_utama=True,
                                                             personil_kegiatan=keg).values_list('peran',
                                                                                                flat=True)[
                                        0] + ']' + ' ' + user.get_full_name()) for user in
                                   User.objects.filter(personil__personil_kegiatan=keg,
                                                       personil__peran__in=['L'],
                                                       personil__wbs_wp_kode=data_peran.wbs_wp_kode).order_by(
                                       'username').distinct().exclude(
                                       pk=request.user.pk)]

    elif data_peran.peran == 'L':
        formulir.fields['penerima'].choices = \
            [('', '-----')] + [(user.pk, '[' +
                                user.personil_set.filter(orang=user.pk, peran_utama=True,
                                                         personil_kegiatan=keg).values_list('peran',
                                                                                            flat=True)[
                                    0] + ']' + ' ' + user.get_full_name()) for user in
                               User.objects.filter(personil__personil_kegiatan=keg,
                                                   personil__peran__in=['ES'],
                                                   personil__wbs_wp_kode=data_peran.wbs_wp_kode).order_by(
                                   'username').distinct().exclude(
                                   pk=request.user.pk)]

    try:
        peran = request.user.personil_set.values_list('peran', flat=True)[0]
    except IndexError:
        peran = ''

    if peran == 'ES':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A', hasil__contains='Lembar Instruksi',
                                                    pelaksana__in=['Pertama', 'Pertama/Muda', 'Muda'])
    elif peran == 'L':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A', hasil__contains='Lembar Instruksi',
                                                    pelaksana__in=['Pertama', 'Pertama/Muda', 'Muda', 'Madya'])
    elif peran == 'GL':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A', hasil__contains='Lembar Instruksi',
                                                    pelaksana__in=['Muda', 'Muda/Madya', 'Madya', 'Utama'])
    elif peran == 'PM':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A', hasil__contains='Lembar Instruksi',
                                                    pelaksana__in=['Muda', 'Muda/Madya', 'Madya', 'Utama'])
    elif peran == 'CE':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A', hasil__contains='Lembar Instruksi',
                                                    pelaksana__in=['Madya', 'Madya/Utama', 'Utama'])
    elif peran == 'PD':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A', hasil__contains='Lembar Instruksi',
                                                    pelaksana__in=['Madya', 'Madya/Utama', 'Utama'])
    else:
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='III.A')

    data = {
        'pk': keg,
        'li': data_li,
        'li_tertentu': li,
        'kegiatan': data_kegiatan,
        'peran': [request.user, keg],
        'formulir': formulir,
        'format': data_format,
        'butir': data_butir,
    }

    if data_peran.peran in ['GL', 'L']:
        return render(request, 'tugas/halaman_li_anggota_modifikasi.html', data)
    else:
        messages.warning(request, 'Hanya dapat dilakukan oleh Group Leader atau Leader')
        return redirect('halaman_li_anggota_rinci', slug=slugify(li.nomor, allow_unicode=True), pk=li.pk, keg=keg)


@login_required
def hapus_li(request, pk):
    li_ubah = get_object_or_404(LembarInstruksi, pk=pk)

    if li_ubah.pemberi == request.user and li_ubah.kesepakatan:
        if li_ubah.delete():
            html = '''<div class="ui green message">
                    <div class="header">
                        Info
                    </div>
                    <p>
                        Lembar instruksi berhasil dihapus.
                    </p>
                </div>'''
            return HttpResponse(html)
    else:
        html = '''<div class="ui red message">
                <div class="header">
                    Info
                </div>
                <p>
                    Lembar instruksi hanya boleh dihapus oleh pemilik dan disetujui oleh bawahan untuk dihapus!
                </p>
            </div>'''
        return HttpResponse(html)


@login_required
def duplikat_li(request, slug, keg, kode, li):
    if slug is None or kode is None:
        pass

    try:
        instruksi = get_object_or_404(LembarInstruksi, pk=li)
    except Http404:
        messages.warning(request, 'Penugasan tidak ditemukan')
        return redirect('halaman_tugas_anggota', pk=keg)

    try:
        instruksi.pk = None
        if cek_keanggotaan(request.user, keg):
            if request.user.username == instruksi.pemberi.username:
                instruksi.save()
                messages.warning(request, 'Lembar instruksi berhasil diduplikat')
                return redirect('halaman_li_anggota_rinci', slug=slugify(instruksi.nomor, allow_unicode=True), pk=li,
                                keg=keg)
            else:
                messages.warning(request, 'Hanya pemberi tugas yang mendapatkan hak akses!')
                return redirect('halaman_tugas_anggota', pk=keg)
        else:
            messages.warning(request, 'Maaf, Anda tidak mendapatkan hak akses!')
            return redirect('halaman_tugas_anggota', pk=keg)
    except Http404:
        messages.warning(request, 'Tugas tidak ditemukan')
        return redirect('halaman_li_anggota_rinci', slug=slugify(instruksi.nomor, allow_unicode=True), pk=li, keg=keg)


@login_required
def kesepakatan_li(request, slug, keg, li):
    if slug is None:
        pass

    try:
        data_li = get_object_or_404(LembarInstruksi, kegiatan=keg, pk=li)
    except Http404:
        messages.warning(request, 'Lemabr instruksi tidak ditemukan!')
        data_li = LembarInstruksi()

    if request.method == 'POST':
        form = FormKesepakatan(request.POST, instance=data_li)

        if form.is_valid():
            messages.success(request, 'Anda setuju ' + data_li.nomor + ' untuk dihapus suatu waktu')
            data_li.save()
    else:
        form = FormKesepakatan(instance=data_li)

    data = {
        'pk': keg,
        'li': data_li,
        'peran': [request.user, keg],
        'formulir': form,
    }

    return render(request, 'tugas/halaman_li_anggota_kesepakatan.html', data)


@login_required
def lihat_lk(request, slug, pk, keg, li):
    if slug is None:
        pass

    try:
        data_lk = get_object_or_404(LembarKerja, pk=pk)
    except Http404:
        messages.warning(request, 'Lembar kerja tidak ditemukan!')
        return redirect('halaman_tugas_anggota', pk=keg)

    try:
        instruksi = get_object_or_404(LembarInstruksi, pk=li)
    except Http404:
        messages.warning(request, 'Penugasan tidak ditemukan')
        return redirect('halaman_tugas_anggota', pk=keg)

    data = {
        'lmbr': data_lk,
        'instruksi': instruksi,
        'pk': keg,
        'li': li,
        'is_exist': False,
    }

    if request.user.username == data_lk.pemberi.username or request.user.username == data_lk.penerima.username:
        return render(request, 'tugas/halaman_lk_anggota_rinci.html', data)
    else:
        messages.warning(request, 'Hanya pemberi dan penerima tugas saja yang memiliki hak akses!')
        return redirect('halaman_tugas_anggota', pk=keg)


@login_required
def lihat_lk_rinci(request, slug, pk, keg):
    if slug is None:
        pass

    try:
        data_li = get_object_or_404(LembarKerja, pk=pk)
    except Http404:
        messages.warning(request, 'Lembar kerja tidak ditemukan!')
        return redirect('halaman_tugas_anggota', pk=keg)

    try:
        data_keg = get_object_or_404(Kegiatan, pk=keg)
    except Http404:
        messages.warning(request, 'Kegiatan/Program tidak ditemukan!')
        return redirect('halaman_tugas_anggota', pk=keg)

    data = {
        'lmbr': data_li,
        'pk': keg,
        'kegiatan': data_keg,
        'peran': [data_li.penerima.pk, data_keg.pk],
        'peran_pemeriksa': [data_li.pemberi.pk, data_keg.pk],
    }

    if data_li.penerima.username == request.user.username or request.user.is_superuser or \
                    data_li.pemberi.username == request.user.username:
        return render(request, 'tugas/halaman_cetak_lk_lembaran.html', data)
    else:
        messages.warning(request, 'Hanya pemilik yang mendapatkan hak akses!')
        # return redirect('/tugas/%s-%s-%s/rincian/' % (slugify(data_li.nomor, allow_unicode=True), pk, keg))
        return redirect('halaman_lk_anggota_rinci', slug=slugify(data_li.nomor, allow_unicode=True), pk=pk, keg=keg,
                        li=data_li.pk)


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def tambah_lk(request, slug, keg, kode, li):
    if slug is None:
        pass

    try:
        data_peran = get_object_or_404(Personil, orang=request.user, personil_kegiatan=keg, peran_utama=True)
    except Http404:
        messages.warning(request, 'Anda tidak memiliki peran dalam kegiatan ini!')
        return redirect('halaman_tugas_anggota', pk=keg)

    try:
        data_kegiatan = get_object_or_404(Kegiatan, pk=keg)
    except Http404:
        messages.warning(request, 'Halaman yang Anda cari tidak ditemukan!')
        return redirect('halaman_tugas_anggota', pk=keg)

    data_li = LembarInstruksi.objects.filter(pk=li).exclude(pemberi=request.user)

    try:
        instruksi = get_object_or_404(LembarInstruksi, pk=li)
    except Http404:
        messages.warning(request, 'Penugasan tidak ditemukan')
        return redirect('halaman_tugas_anggota', pk=keg)

    try:
        data_format = get_object_or_404(Format, format_kegiatan=keg, kode=kode)

    except Http404:
        messages.warning(request, 'Format lembar instruksi tidak ditemukan...')
        return redirect('halaman_tugas_anggota', pk=keg)

    if request.method == 'POST':
        butir = request.POST.get('butir')
        angka = request.POST.get('angka_hid')
        cek_angka = round(bantu_butir_perekayasa(request, butir, keg, 'na'), 3)

        a = LembarKerja(kegiatan=Kegiatan.objects.get(pk=keg), penerima=request.user, angka=angka, li=instruksi)

        formulir = FormLK(request.POST, instance=a)

        if formulir.is_valid():
            if cek_keanggotaan(request.user, keg):
                if request.user.username != instruksi.pemberi.username:
                    if float(angka) == cek_angka:
                        messages.success(request, 'Lembar kerja berhasil ditambahkan')
                        a.save()
                    else:
                        messages.warning(request, 'Tidak diperbolehkan untuk mengganti angka kredit!')
                        return redirect('halaman_tambah_lk_anggota', slug=slug, keg=keg, kode=kode, li=li)
                else:
                    messages.warning(request, 'Tidak diperbolehkan untuk mengganti angka kredit!')
                    return redirect('halaman_tambah_lk_anggota', slug=slug, keg=keg, kode=kode, li=li)
            else:
                messages.warning(request, 'Maaf, Anda tidak mendapatkan hak akses!')
                return redirect('halaman_tugas_anggota', pk=keg)

    else:
        formulir = FormLK()

    if data_peran.peran == 'L':
        formulir.fields['pemberi'].choices = \
            [('', '-----')] + [(user.pk, '[' +
                                user.personil_set.filter(orang=user.pk, peran_utama=True,
                                                         personil_kegiatan=keg).values_list('peran',
                                                                                            flat=True)[
                                    0] + ']' + ' ' + user.get_full_name()) for user in
                               User.objects.filter(personil__personil_kegiatan=keg,
                                                   personil__peran__in=['GL']).order_by(
                                   'username').distinct().exclude(
                                   pk=request.user.pk)]
    else:
        formulir.fields['pemberi'].choices = \
            [('', '-----')] + [(user.pk, '[' +
                                user.personil_set.filter(orang=user.pk, peran_utama=True,
                                                         personil_kegiatan=keg).values_list('peran',
                                                                                            flat=True)[
                                    0] + ']' + ' ' + user.get_full_name()) for user in
                               User.objects.filter(personil__personil_kegiatan=keg,
                                                   personil__peran__in=['L'],
                                                   personil__wbs_wp_kode=data_peran.wbs_wp_kode).order_by(
                                   'username').distinct().exclude(
                                   pk=request.user.pk)]

    formulir.fields['lb'].choices = [('', '-----')] + [(lb.pk, lb.nomor) for lb in
                                                       Logbook.objects.filter(kegiatan=keg, li=li)]

    try:
        peran = request.user.personil_set.values_list('peran', flat=True)[0]
    except IndexError:
        peran = ''

    if peran == 'ES':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A',
                                                    hasil__contains='Lembar Kerja',
                                                    pelaksana__in=['Pertama', 'Pertama/Muda', 'Muda'])
    elif peran == 'L':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A', hasil__contains='Lembar Kerja',
                                                    pelaksana__in=['Pertama', 'Pertama/Muda', 'Muda', 'Madya'])
    elif peran == 'GL':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A', hasil__contains='Lembar Kerja',
                                                    pelaksana__in=['Muda', 'Muda/Madya', 'Madya', 'Utama'])
    elif peran == 'PM':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A', hasil__contains='Lembar Kerja',
                                                    pelaksana__in=['Muda', 'Muda/Madya', 'Madya', 'Utama'])
    elif peran == 'CE':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A', hasil__contains='Lembar Kerja',
                                                    pelaksana__in=['Madya', 'Madya/Utama', 'Utama'])
    elif peran == 'PD':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A', hasil__contains='Lembar Kerja',
                                                    pelaksana__in=['Madya', 'Madya/Utama', 'Utama'])
    else:
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='III.A')

    data = {
        'pk': keg,
        'li': data_li,
        'instruksi': instruksi,
        'kegiatan': data_kegiatan,
        'peran': [request.user, keg],
        'formulir': formulir,
        'format': data_format,
        'butir': data_butir,
    }

    if data_peran.peran in ['L', 'ES']:
        return render(request, 'tugas/halaman_li_anggota_modifikasi.html', data)
    else:
        messages.warning(request, 'Hanya dapat dilakukan oleh Leader atau Engineering Staff')
        return redirect('halaman_tugas_anggota', pk=keg)


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ubah_lk(request, slug, keg, kode, li, lk):
    if slug is None:
        pass

    try:
        data_peran = get_object_or_404(Personil, orang=request.user, personil_kegiatan=keg, peran_utama=True)
    except Http404:
        messages.warning(request, 'Anda tidak memiliki peran dalam kegiatan ini!')
        return redirect('halaman_tugas_anggota', pk=keg)

    try:
        data_kegiatan = get_object_or_404(Kegiatan, pk=keg)
    except Http404:
        messages.warning(request, 'Halaman yang Anda cari tidak ditemukan!')
        return redirect('halaman_tugas_anggota', pk=keg)

    data_li = LembarInstruksi.objects.filter(pk=li).exclude(pemberi=request.user)

    try:
        instruksi = get_object_or_404(LembarInstruksi, pk=li)
    except Http404:
        messages.warning(request, 'Penugasan tidak ditemukan')
        return redirect('halaman_tugas_anggota', pk=keg)

    try:
        kerja = get_object_or_404(LembarKerja, pk=lk)
    except Http404:
        messages.warning(request, 'Tugas tidak ditemukan')
        return redirect('halaman_li_anggota_rinci', slug=slugify(data_li.nomor, allow_unicode=True), pk=li, keg=keg)

    try:
        data_format = get_object_or_404(Format, format_kegiatan=keg, kode=kode)

    except Http404:
        messages.warning(request, 'Format lembar instruksi tidak ditemukan...')
        return redirect('halaman_tugas_anggota', pk=keg)

    if request.method == 'POST':
        butir = request.POST.get('butir')
        angka = request.POST.get('angka_hid')
        cek_angka = round(bantu_butir_perekayasa(request, butir, keg, 'na'), 3)

        kerja.angka = float(angka)

        formulir = FormLK(request.POST, instance=kerja)

        if formulir.is_valid():
            if cek_keanggotaan(request.user, keg):
                if request.user.username != instruksi.pemberi.username:
                    if float(angka) == cek_angka:
                        if butir not in ['II.A.1.a.2).(b)', 'II.A.1.a.4).(a)', 'II.A.1.a.4).(b)', 'II.A.1.a.4).(c)',
                                         'II.A.1.a.6).(c)', 'II.A.1.a.7).(c)', 'II.A.1.a.8).(c)']:
                            kerja.lb = None

                        messages.success(request, 'Lembar kerja berhasil disimpan')
                        kerja.save()
                    else:
                        messages.warning(request, 'Tidak diperbolehkan untuk mengganti angka kredit!')
                        return redirect('halaman_lk_anggota_rinci', slug=slug, pk=kerja.pk, keg=keg, li=li)
                else:
                    messages.warning(request, 'Hanya penerima instruksi yang mendapatkan hak akses!')
                    return redirect('halaman_lk_anggota_rinci', slug=slug, pk=kerja.pk, keg=keg, li=li)
            else:
                messages.warning(request, 'Maaf, Anda tidak mendapatkan hak akses!')
                return redirect('halaman_tugas_anggota', pk=keg)

    else:
        formulir = FormLK(instance=kerja)

    if data_peran.peran == 'L':
        formulir.fields['pemberi'].choices = \
            [('', '-----')] + [(user.pk, '[' +
                                user.personil_set.filter(orang=user.pk, peran_utama=True,
                                                         personil_kegiatan=keg).values_list('peran',
                                                                                            flat=True)[
                                    0] + ']' + ' ' + user.get_full_name()) for user in
                               User.objects.filter(personil__personil_kegiatan=keg,
                                                   personil__peran__in=['GL']).order_by(
                                   'username').distinct().exclude(
                                   pk=request.user.pk)]
    else:
        formulir.fields['pemberi'].choices = \
            [('', '-----')] + [(user.pk, '[' +
                                user.personil_set.filter(orang=user.pk, peran_utama=True,
                                                         personil_kegiatan=keg).values_list('peran',
                                                                                            flat=True)[
                                    0] + ']' + ' ' + user.get_full_name()) for user in
                               User.objects.filter(personil__personil_kegiatan=keg,
                                                   personil__peran__in=['L'],
                                                   personil__wbs_wp_kode=data_peran.wbs_wp_kode).order_by(
                                   'username').distinct().exclude(
                                   pk=request.user.pk)]

    formulir.fields['lb'].choices = [('', '-----')] + [(lb.pk, lb.nomor) for lb in
                                                       Logbook.objects.filter(kegiatan=keg, li=li, butir=kerja.butir)]

    try:
        peran = request.user.personil_set.values_list('peran', flat=True)[0]
    except IndexError:
        peran = ''

    if peran == 'ES':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A',
                                                    hasil__contains='Lembar Kerja',
                                                    pelaksana__in=['Pertama', 'Pertama/Muda', 'Muda'])
    elif peran == 'L':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A', hasil__contains='Lembar Kerja',
                                                    pelaksana__in=['Pertama', 'Pertama/Muda', 'Muda', 'Madya'])
    elif peran == 'GL':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A', hasil__contains='Lembar Kerja',
                                                    pelaksana__in=['Muda', 'Muda/Madya', 'Madya', 'Utama'])
    elif peran == 'PM':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A', hasil__contains='Lembar Kerja',
                                                    pelaksana__in=['Muda', 'Muda/Madya', 'Madya', 'Utama'])
    elif peran == 'CE':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A', hasil__contains='Lembar Kerja',
                                                    pelaksana__in=['Madya', 'Madya/Utama', 'Utama'])
    elif peran == 'PD':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A', hasil__contains='Lembar Kerja',
                                                    pelaksana__in=['Madya', 'Madya/Utama', 'Utama'])
    else:
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='III.A')

    data = {
        'pk': keg,
        'li': data_li,
        'lk': lk,
        'instruksi': instruksi,
        'li_tertentu': instruksi,
        'kegiatan': data_kegiatan,
        'peran': [request.user, keg],
        'formulir': formulir,
        'format': data_format,
        'butir': data_butir,
    }

    if data_peran.peran in ['L', 'ES']:
        return render(request, 'tugas/halaman_li_anggota_modifikasi.html', data)
    else:
        messages.warning(request, 'Hanya dapat dilakukan oleh Leader atau Engineering Staff')
        return redirect('halaman_tugas_anggota', pk=keg)


@login_required
def duplikat_lk(request, slug, keg, kode, li, lk):
    if slug is None or kode is None:
        pass

    try:
        instruksi = get_object_or_404(LembarInstruksi, pk=li)
    except Http404:
        messages.warning(request, 'Penugasan tidak ditemukan')
        return redirect('halaman_tugas_anggota', pk=keg)

    try:
        kerja = get_object_or_404(LembarKerja, pk=lk)
    except Http404:
        messages.warning(request, 'Tugas tidak ditemukan')
        return redirect('halaman_li_anggota_rinci', slug=slugify(instruksi.nomor, allow_unicode=True), pk=li, keg=keg)

    try:
        duplikat = get_object_or_404(LembarKerja, pk=lk)
        duplikat.pk = None
        if cek_keanggotaan(request.user, keg):
            if request.user.username == instruksi.penerima.username:
                duplikat.save()
                messages.warning(request, 'Lembar kerja berhasil diduplikat')
                return redirect('halaman_lk_anggota_rinci', slug=slug, pk=kerja.pk, keg=keg, li=li)
            else:
                messages.warning(request, 'Hanya penerima tugas yang mendapatkan hak akses!')
                return redirect('halaman_lk_anggota_rinci', slug=slug, pk=kerja.pk, keg=keg, li=li)
        else:
            messages.warning(request, 'Maaf, Anda tidak mendapatkan hak akses!')
            return redirect('halaman_tugas_anggota', pk=keg)
    except Http404:
        messages.warning(request, 'Tugas tidak ditemukan')
        return redirect('halaman_li_anggota_rinci', slug=slugify(instruksi.nomor, allow_unicode=True), pk=li, keg=keg)


@login_required
def hapus_lk(request, pk):
    lk_ubah = get_object_or_404(LembarKerja, pk=pk)

    if lk_ubah.penerima == request.user:
        if lk_ubah.delete():
            html = '''<div class="ui green message">
                    <div class="header">
                        Info
                    </div>
                    <p>
                        Lembar kerja berhasil dihapus.
                    </p>
                </div>'''
            return HttpResponse(html)
    else:
        html = '''<div class="ui red message">
                <div class="header">
                    Info
                </div>
                <p>
                    Lembar kerja hanya boleh dihapus oleh pemilik!
                </p>
            </div>'''
        return HttpResponse(html)
