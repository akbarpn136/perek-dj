from django.shortcuts import render, redirect, get_object_or_404, Http404, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.cache import cache_control
from django.utils.text import slugify

from tugas.models import LembarInstruksi, Kegiatan, Logbook
from utama.models import Format, Personil
from butir.models import ButirPerekayasa
from utiliti.models import Profil

from .forms import FormLB


# Create your views here.
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


def bantu_pilih_lb(request, cond):
    data_raw = {
        'lb': [(lb.pk, lb.nomor) for lb in Logbook.objects.filter(butir=cond)]
    }

    return JsonResponse(data_raw, safe=False)


def cek_keanggotaan(user, pk_kegiatan):
    anggota_kegiatan = User.objects.filter(personil__personil_kegiatan=pk_kegiatan)
    return user.pk in anggota_kegiatan.values_list('pk', flat=True)


@login_required
def lihat_lb(request, slug, pk, keg, li):
    if slug is None:
        pass

    try:
        data_lb = get_object_or_404(Logbook, pk=pk, kegiatan=keg, li=li)
    except Http404:
        messages.warning(request, 'Logbook tidak ditemukan!')
        return redirect('halaman_tugas_anggota', pk=keg)

    try:
        instruksi = get_object_or_404(LembarInstruksi, pk=li)
    except Http404:
        messages.warning(request, 'Penugasan tidak ditemukan')
        return redirect('halaman_tugas_anggota', pk=keg)

    data = {
        'lmbr': data_lb,
        'instruksi': instruksi,
        'pk': keg,
        'li': li,
        'is_exist': False,
    }

    if request.user.username == data_lb.pemberi.username or request.user.username == data_lb.penerima.username:
        return render(request, 'logbook/halaman_lb_anggota_rinci.html', data)
    else:
        messages.warning(request, 'Hanya pemberi dan penerima tugas saja yang memiliki hak akses!')
        return redirect('halaman_tugas_anggota', pk=keg)


@login_required
def lihat_lb_rinci(request, slug, pk, keg, kode):
    if slug is None:
        pass

    try:
        data_lb = get_object_or_404(Logbook, pk=pk)
    except Http404:
        messages.warning(request, 'Logbook tidak ditemukan!')
        return redirect('halaman_tugas_anggota', pk=keg)

    try:
        data_keg = get_object_or_404(Kegiatan, pk=keg)
    except Http404:
        messages.warning(request, 'Kegiatan/Program tidak ditemukan!')
        return redirect('halaman_tugas_anggota', pk=keg)

    prof = get_object_or_404(Profil, user=request.user)

    data = {
        'lmbr': data_lb,
        'kegiatan': data_keg,
        'profil': prof,
        'peran': [data_lb.penerima.pk, data_keg.pk],
        'peran_pemberi': [data_lb.pemberi.pk, data_keg.pk],
        'peran_pemeriksa': [data_lb.pemeriksa.pk, data_keg.pk],
    }

    if kode == 'cover':
        data['status'] = True
    else:
        data['status'] = False

    if data_lb.penerima.username == request.user.username or request.user.is_superuser or \
            data_lb.pemberi.username == request.user.username:
        return render(request, 'logbook/halaman_cetak_lb_lembaran.html', data)
    else:
        messages.warning(request, 'Hanya pemilik yang mendapatkan hak akses!')
        # return redirect('/tugas/%s-%s-%s/rincian/' % (slugify(data_li.nomor, allow_unicode=True), pk, keg))
        return redirect('halaman_lk_anggota_rinci', slug=slugify(data_lb.nomor, allow_unicode=True), pk=pk, keg=keg,
                        li=data_lb.pk)


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def tambah_lb(request, slug, keg, kode, li):
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
        messages.warning(request, 'Kegiatan tidak ditemukan')
        return redirect('halaman_tugas_anggota', pk=keg)

    try:
        instruksi = get_object_or_404(LembarInstruksi, pk=li)
    except Http404:
        messages.warning(request, 'Penugasan tidak ditemukan')
        return redirect('halaman_tugas_anggota', pk=keg)

    try:
        data_format = get_object_or_404(Format, format_kegiatan=keg, kode=kode)

    except Http404:
        messages.warning(request, 'Format logbook tidak ditemukan...')
        return redirect('halaman_tugas_anggota', pk=keg)

    if request.method == 'POST':
        butir = request.POST.get('butir')
        angka = request.POST.get('angka_hid')
        cek_angka = round(bantu_butir_perekayasa(request, butir, keg, 'na'), 3)

        a = Logbook(kegiatan=Kegiatan.objects.get(pk=keg), penerima=request.user, angka=angka, li=instruksi)

        formulir = FormLB(request.POST, instance=a)

        if formulir.is_valid():
            if cek_keanggotaan(request.user, keg):
                if request.user.username != instruksi.pemberi.username:
                    if float(angka) == cek_angka:
                        messages.success(request, 'Logbook berhasil ditambahkan')
                        a.save()
                    else:
                        messages.warning(request, 'Tidak diperbolehkan untuk mengganti angka kredit!')
                        return redirect('halaman_li_anggota_rinci', slug=slug, pk=li, keg=keg)
                else:
                    messages.warning(request, 'Tidak diperbolehkan untuk mengganti angka kredit!')
                    return redirect('halaman_li_anggota_rinci', slug=slug, pk=li, keg=keg)
            else:
                messages.warning(request, 'Maaf, Anda tidak mendapatkan hak akses!')
                return redirect('halaman_tugas_anggota', pk=keg)

    else:
        formulir = FormLB()

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

    formulir.fields['pemeriksa'].choices = \
        [('', '-----')] + [(user.pk, '[' +
                            user.personil_set.filter(orang=user.pk, peran_utama=True,
                                                     personil_kegiatan=keg).values_list('peran',
                                                                                        flat=True)[
                                0] + ']' + ' ' + user.get_full_name()) for user in
                           User.objects.filter(personil__personil_kegiatan=keg,
                                               personil__peran__in=['GL']).order_by(
                               'username').distinct().exclude(
                               pk=request.user.pk)]

    try:
        peran = request.user.personil_set.values_list('peran', flat=True)[0]
    except IndexError:
        peran = ''

    if peran == 'ES':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A',
                                                    hasil__contains='Logbook',
                                                    pelaksana__in=['Pertama', 'Pertama/Muda', 'Muda'])
    elif peran == 'L':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A', hasil__contains='Logbook',
                                                    pelaksana__in=['Pertama', 'Pertama/Muda', 'Muda', 'Madya'])
    elif peran == 'GL':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A', hasil__contains='Logbook',
                                                    pelaksana__in=['Muda', 'Muda/Madya', 'Madya', 'Utama'])
    elif peran == 'PM':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A', hasil__contains='Logbook',
                                                    pelaksana__in=['Muda', 'Muda/Madya', 'Madya', 'Utama'])
    elif peran == 'CE':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A', hasil__contains='Logbook',
                                                    pelaksana__in=['Madya', 'Madya/Utama', 'Utama'])
    elif peran == 'PD':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A', hasil__contains='Logbook',
                                                    pelaksana__in=['Madya', 'Madya/Utama', 'Utama'])
    else:
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='III.A')

    data = {
        'pk': keg,
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
def ubah_lb(request, slug, keg, kode, li, lb):
    if slug is None:
        pass

    try:
        data_logbook = get_object_or_404(Logbook, kegiatan=keg, li=li, pk=lb)
    except Http404:
        messages.warning(request, 'Logbook tidak ditemukan')
        return redirect('halaman_tugas_anggota', pk=keg)

    try:
        data_peran = get_object_or_404(Personil, orang=request.user, personil_kegiatan=keg, peran_utama=True)
    except Http404:
        messages.warning(request, 'Anda tidak memiliki peran dalam kegiatan ini!')
        return redirect('halaman_tugas_anggota', pk=keg)

    try:
        data_kegiatan = get_object_or_404(Kegiatan, pk=keg)
    except Http404:
        messages.warning(request, 'Kegiatan tidak ditemukan')
        return redirect('halaman_tugas_anggota', pk=keg)

    try:
        instruksi = get_object_or_404(LembarInstruksi, pk=li)
    except Http404:
        messages.warning(request, 'Penugasan tidak ditemukan')
        return redirect('halaman_tugas_anggota', pk=keg)

    try:
        data_format = get_object_or_404(Format, format_kegiatan=keg, kode=kode)

    except Http404:
        messages.warning(request, 'Format logbook tidak ditemukan...')
        return redirect('halaman_tugas_anggota', pk=keg)

    if request.method == 'POST':
        butir = request.POST.get('butir')
        angka = request.POST.get('angka_hid')
        cek_angka = round(bantu_butir_perekayasa(request, butir, keg, 'na'), 3)

        formulir = FormLB(request.POST, instance=data_logbook)

        if formulir.is_valid():
            if cek_keanggotaan(request.user, keg):
                if request.user.username != instruksi.pemberi.username:
                    if float(angka) == cek_angka:
                        data_logbook.angka = float(angka)
                        messages.success(request, 'Logbook berhasil disimpan')
                        data_logbook.save()
                    else:
                        messages.warning(request, 'Tidak diperbolehkan untuk mengganti angka kredit!')
                        return redirect('halaman_li_anggota_rinci', slug=slug, pk=li, keg=keg)
                else:
                    messages.warning(request, 'Tidak diperbolehkan untuk mengganti angka kredit!')
                    return redirect('halaman_li_anggota_rinci', slug=slug, pk=li, keg=keg)
            else:
                messages.warning(request, 'Maaf, Anda tidak mendapatkan hak akses!')
                return redirect('halaman_tugas_anggota', pk=keg)

    else:
        formulir = FormLB(instance=data_logbook)

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

    formulir.fields['pemeriksa'].choices = \
        [('', '-----')] + [(user.pk, '[' +
                            user.personil_set.filter(orang=user.pk, peran_utama=True,
                                                     personil_kegiatan=keg).values_list('peran',
                                                                                        flat=True)[
                                0] + ']' + ' ' + user.get_full_name()) for user in
                           User.objects.filter(personil__personil_kegiatan=keg,
                                               personil__peran__in=['GL']).order_by(
                               'username').distinct().exclude(
                               pk=request.user.pk)]

    try:
        peran = request.user.personil_set.values_list('peran', flat=True)[0]
    except IndexError:
        peran = ''

    if peran == 'ES':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A',
                                                    hasil__contains='Logbook',
                                                    pelaksana__in=['Pertama', 'Pertama/Muda', 'Muda'])
    elif peran == 'L':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A', hasil__contains='Logbook',
                                                    pelaksana__in=['Pertama', 'Pertama/Muda', 'Muda', 'Madya'])
    elif peran == 'GL':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A', hasil__contains='Logbook',
                                                    pelaksana__in=['Muda', 'Muda/Madya', 'Madya', 'Utama'])
    elif peran == 'PM':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A', hasil__contains='Logbook',
                                                    pelaksana__in=['Muda', 'Muda/Madya', 'Madya', 'Utama'])
    elif peran == 'CE':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A', hasil__contains='Logbook',
                                                    pelaksana__in=['Madya', 'Madya/Utama', 'Utama'])
    elif peran == 'PD':
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='II.A', hasil__contains='Logbook',
                                                    pelaksana__in=['Madya', 'Madya/Utama', 'Utama'])
    else:
        data_butir = ButirPerekayasa.objects.filter(kodebutir__startswith='III.A')

    data = {
        'pk': keg,
        'instruksi': instruksi,
        'li_tertentu': instruksi,
        'lb': data_logbook,
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
def hapus_lb(request, pk):
    lb_ubah = get_object_or_404(Logbook, pk=pk)

    if lb_ubah.penerima == request.user:
        if lb_ubah.delete():
            html = '''<div class="ui green message">
                    <div class="header">
                        Info
                    </div>
                    <p>
                        Logbook berhasil dihapus.
                    </p>
                </div>'''
            return HttpResponse(html)
    else:
        html = '''<div class="ui red message">
                <div class="header">
                    Info
                </div>
                <p>
                    Logbook hanya boleh dihapus oleh pemilik!
                </p>
            </div>'''
        return HttpResponse(html)


@login_required
def duplikat_lb(request, slug, keg, kode, li, lb):
    if slug is None or kode is None:
        pass

    try:
        instruksi = get_object_or_404(LembarInstruksi, pk=li)
    except Http404:
        messages.warning(request, 'Penugasan tidak ditemukan')
        return redirect('halaman_tugas_anggota', pk=keg)

    try:
        duplikat = get_object_or_404(Logbook, pk=lb)
        duplikat.pk = None
        if cek_keanggotaan(request.user, keg):
            if request.user.username == instruksi.penerima.username:
                duplikat.save()
                messages.warning(request, 'Logbook berhasil diduplikat')
                return redirect('halaman_lb_anggota_rinci', slug=slug, pk=duplikat.pk, keg=keg, li=li)
            else:
                messages.warning(request, 'Hanya penerima tugas yang mendapatkan hak akses!')
                return redirect('halaman_lb_anggota_rinci', slug=slug, pk=duplikat.pk, keg=keg, li=li)
        else:
            messages.warning(request, 'Maaf, Anda tidak mendapatkan hak akses!')
            return redirect('halaman_tugas_anggota', pk=keg)
    except Http404:
        messages.warning(request, 'Tugas tidak ditemukan')
        return redirect('halaman_li_anggota_rinci', slug=slugify(instruksi.nomor, allow_unicode=True), pk=li, keg=keg)
