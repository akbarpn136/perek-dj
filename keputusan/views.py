from tugas.perekayasa import *
from django.shortcuts import get_object_or_404, Http404, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import generic, View
from django.views.generic import edit
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy

from .models import LembarKeputusan
from utama.models import Kegiatan, Personil, Format
from .forms import FormKeputusan


# Create your views here.
@method_decorator(login_required, name='dispatch')
class LihatKeputusan(generic.ListView):
    model = LembarKeputusan
    template_name = 'keputusan/halaman_keputusan.html'
    context_object_name = 'keputusan'
    paginate_by = 12
    paginate_orphans = 1
    page_kwarg = 'halaman'

    def dispatch(self, request, *args, **kwargs):
        if cek_keanggotaan(request.user, self.kwargs['pk']):
            return super(LihatKeputusan, self).dispatch(request, *args, **kwargs)
        else:
            messages.warning(request, 'Maaf, Anda tidak memiliki hak keanggotaan dari kegiatan ini.')
            return redirect('halaman_utama')

    def get_context_data(self, **kwargs):
        context = super(LihatKeputusan, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['kegiatan'] = get_object_or_404(Kegiatan, pk=self.kwargs['pk'])

        return context


@method_decorator(login_required, name='dispatch')
class RincianKeputusan(generic.DetailView):
    model = LembarKeputusan
    template_name = 'keputusan/halaman_cetak_keputusan_lembaran.html'
    context_object_name = 'keputusan'

    def dispatch(self, request, *args, **kwargs):
        if cek_keanggotaan(request.user, self.kwargs['pk_kegiatan']):
            return super(RincianKeputusan, self).dispatch(request, *args, **kwargs)
        else:
            messages.warning(request, 'Maaf, Anda tidak memiliki hak keanggotaan dari kegiatan ini.')
            return redirect('halaman_utama')

    def get_context_data(self, **kwargs):
        try:
            data_kegiatan = get_object_or_404(Kegiatan, pk=self.kwargs['pk_kegiatan'])
        except Http404:
            messages.warning(self.request, 'Halaman yang Anda cari tidak ditemukan')
            return redirect('halaman_utama')

        try:
            data_keputusan = get_object_or_404(LembarKeputusan, pk=self.kwargs['pk'])
        except Http404:
            messages.warning(self.request, 'Halaman yang Anda cari tidak ditemukan')
            return redirect('halaman_utama')

        context = super(RincianKeputusan, self).get_context_data(**kwargs)
        context['peran'] = [data_keputusan.pemberi, data_kegiatan.pk]

        return context


@method_decorator(login_required, name='dispatch')
class TambahKeputusan(edit.CreateView):
    model = LembarKeputusan
    template_name = 'keputusan/halaman_keputusan_anggota_modifikasi.html'
    form_class = FormKeputusan

    def dispatch(self, request, *args, **kwargs):
        if cek_keanggotaan(request.user, self.kwargs['pk']):
            try:
                data_peran = get_object_or_404(Personil, orang=request.user, personil_kegiatan=self.kwargs['pk'],
                                               peran_utama=True)
                peran = data_peran.peran
            except Http404:
                peran = ''

            if peran not in ['TS', 'ES', 'ACE']:
                return super(TambahKeputusan, self).dispatch(request, *args, **kwargs)
            else:
                messages.warning(request, 'Maaf, Anda tidak mendapatkan izin untuk tambah surat keputusan')
                return redirect('halaman_utama')
        else:
            messages.warning(request, 'Maaf, Anda tidak memiliki hak keanggotaan dari kegiatan ini.')
            return redirect('halaman_utama')

    def get_initial(self):
        return {'pemberi': self.request.user}

    def get_context_data(self, **kwargs):
        try:
            data_kegiatan = get_object_or_404(Kegiatan, pk=self.kwargs['pk'])
        except Http404:
            messages.warning(self.request, 'Halaman yang Anda cari tidak ditemukan')
            return redirect('halaman_utama')

        try:
            data_format = get_object_or_404(Format, format_kegiatan=self.kwargs['pk'], kode='DS')
        except Http404:
            messages.warning(self.request, 'Halaman yang Anda cari tidak ditemukan')
            return redirect('halaman_utama')

        data_butir = bantu_peran(self.request.user, 'Lembar Keputusan')

        context = super(TambahKeputusan, self).get_context_data(**kwargs)
        context['peran'] = [self.request.user, data_kegiatan.pk]
        context['pk'] = data_kegiatan.pk
        context['kegiatan'] = data_kegiatan
        context['butir'] = data_butir
        context['format'] = data_format

        return context

    def get_form(self, form_class=None):
        form = super(TambahKeputusan, self).get_form(form_class)
        form.fields['pemberi'].choices = [('', '------')] + [(user.pk, user.get_full_name()) for user in
                                                             User.objects.filter(
                                                                 personil__personil_kegiatan=self.kwargs['pk']
                                                             ).distinct()]

        return form

    def form_valid(self, form):
        butir = self.request.POST.get('butir')
        angka = self.request.POST.get('angka_hid')
        cek_angka = round(bantu_butir_perekayasa(self.request, butir, self.kwargs['pk'], 'na'), 3)

        if float(angka) == cek_angka:
            form.instance.angka = angka
            form.instance.kegiatan = Kegiatan.objects.get(pk=self.kwargs['pk'])
            form.instance.pemberi = self.request.user

            messages.success(self.request, 'Lembar keputusan berhasil ditambahkan')
            return super(TambahKeputusan, self).form_valid(form)
        else:
            messages.warning(self.request, 'Tidak diperbolehkan untuk mengganti angka kredit!')
            return redirect('halaman_keputusan', slug=self.kwargs['slug'], keg=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('halaman_keputusan', kwargs={'slug': self.kwargs['slug'], 'pk': self.kwargs['pk']})


@method_decorator(login_required, name='dispatch')
class UbahKeputusan(edit.UpdateView):
    model = LembarKeputusan
    template_name = 'keputusan/halaman_keputusan_anggota_modifikasi.html'
    form_class = FormKeputusan

    def dispatch(self, request, *args, **kwargs):
        if cek_keanggotaan(request.user, self.kwargs['pk_kegiatan']):
            try:
                data_peran = get_object_or_404(Personil, orang=request.user,
                                               personil_kegiatan=self.kwargs['pk_kegiatan'], peran_utama=True)
                peran = data_peran.peran
            except Http404:
                peran = ''

            try:
                data_pemberi = get_object_or_404(LembarKeputusan, kegiatan=self.kwargs['pk_kegiatan'],
                                                 pk=self.kwargs['pk'])
            except Http404:
                messages.warning(request, 'Halaman tidak ditemukan.')
                return redirect('halaman_utama')

            if peran not in ['TS', 'ES', 'ACE']:
                if data_pemberi.pemberi == request.user:
                    return super(UbahKeputusan, self).dispatch(request, *args, **kwargs)
                else:
                    messages.warning(request, 'Hanya pimpinan rapat yang mendapatkan hak akses.')
                    return redirect('halaman_keputusan', slug=self.kwargs['slug'], pk=self.kwargs['pk_kegiatan'])
            else:
                messages.warning(request, 'Maaf, Anda tidak mendapatkan izin untuk tambah surat keputusan')
                return redirect('halaman_utama')
        else:
            messages.warning(request, 'Maaf, Anda tidak memiliki hak keanggotaan dari kegiatan ini.')
            return redirect('halaman_utama')

    def get_context_data(self, **kwargs):
        try:
            data_kegiatan = get_object_or_404(Kegiatan, pk=self.kwargs['pk_kegiatan'])
        except Http404:
            messages.warning(self.request, 'Halaman yang Anda cari tidak ditemukan')
            return redirect('halaman_utama')

        try:
            data_format = get_object_or_404(Format, format_kegiatan=self.kwargs['pk_kegiatan'], kode='DS')
        except Http404:
            messages.warning(self.request, 'Halaman yang Anda cari tidak ditemukan')
            return redirect('halaman_utama')

        data_butir = bantu_peran(self.request.user, 'Lembar Keputusan')

        context = super(UbahKeputusan, self).get_context_data(**kwargs)
        context['peran'] = [self.request.user, data_kegiatan.pk]
        context['pk'] = data_kegiatan.pk
        context['pk_keputusan'] = self.kwargs['pk']
        context['kegiatan'] = data_kegiatan
        context['butir'] = data_butir
        context['format'] = data_format

        return context

    def get_form(self, form_class=None):
        form = super(UbahKeputusan, self).get_form(form_class)
        form.fields['pemberi'].choices = [('', '------')] + [(user.pk, user.get_full_name()) for user in
                                                             User.objects.filter(
                                                                 personil__personil_kegiatan=self.kwargs['pk_kegiatan']
                                                             ).distinct()]

        return form

    def form_valid(self, form):
        butir = self.request.POST.get('butir')
        angka = self.request.POST.get('angka_hid')
        cek_angka = round(bantu_butir_perekayasa(self.request, butir, self.kwargs['pk_kegiatan'], 'na'), 3)

        if float(angka) == cek_angka:
            form.instance.angka = angka
            form.instance.kegiatan = Kegiatan.objects.get(pk=self.kwargs['pk_kegiatan'])
            form.instance.pemberi = self.request.user

            messages.success(self.request, 'Lembar keputusan berhasil disimpan.')
            return super(UbahKeputusan, self).form_valid(form)
        else:
            messages.warning(self.request, 'Tidak diperbolehkan untuk mengganti angka kredit!')
            return redirect('halaman_keputusan', slug=self.kwargs['slug'], keg=self.kwargs['pk_kegiatan'])

    def get_success_url(self):
        return reverse_lazy('halaman_keputusan',
                            kwargs={'slug': self.kwargs['slug'], 'pk': self.kwargs['pk_kegiatan']})


@method_decorator(login_required, name='dispatch')
class HapusKeputusan(View):
    def get(self, request, **kwargs):
        if cek_keanggotaan(request.user, kwargs['pk_kegiatan']):
            try:
                kep = get_object_or_404(LembarKeputusan, kegiatan=self.kwargs['pk_kegiatan'], pk=self.kwargs['pk'])

                if kep.pemberi == request.user:
                    if kep.delete():
                        html = '''<div class="ui green message">
                                <div class="header">
                                    Info
                                </div>
                                <p>
                                    Lembar keputusan berhasil dihapus.
                                </p>
                            </div>'''
                        return HttpResponse(html)
                else:
                    messages.warning(request, 'Hanya pemilik yang dapat hak akses.')
                    return redirect('halaman_keputusan', slug=kwargs['slug'], pk=kwargs['pk_kegiatan'])
            except Http404:
                messages.warning(request, 'Halaman yang Anda cari tidak ditemukan.')
                return redirect('halaman_keputusan', slug=kwargs['slug'], pk=kwargs['pk_kegiatan'])

        else:
            html = '''<div class="ui red message">
                <div class="header">
                    Info
                </div>
                <p>
                    Anda tidak memiliki hak akses.
                </p>
            </div>'''
            return HttpResponse(html)


@method_decorator(login_required, name='dispatch')
class DuplikatKeputusan(View):
    def get(self, request, **kwargs):
        if cek_keanggotaan(request.user, kwargs['pk_kegiatan']):
            try:
                kep = get_object_or_404(LembarKeputusan, kegiatan=self.kwargs['pk_kegiatan'], pk=self.kwargs['pk'])
                kep.pk = None

                if kep.pemberi == request.user:
                    kep.save()
                    messages.success(request, 'Surat keputusan berhasil diduplikat.')
                    return redirect('halaman_keputusan', slug=kwargs['slug'], pk=kwargs['pk_kegiatan'])
                else:
                    messages.warning(request, 'Hanya pemilik yang dapat hak akses.')
                    return redirect('halaman_keputusan', slug=kwargs['slug'], pk=kwargs['pk_kegiatan'])
            except Http404:
                messages.warning(request, 'Halaman yang Anda cari tidak ditemukan.')
                return redirect('halaman_keputusan', slug=kwargs['slug'], pk=kwargs['pk_kegiatan'])

        else:
            html = '''<div class="ui red message">
                <div class="header">
                    Info
                </div>
                <p>
                    Anda tidak memiliki hak akses.
                </p>
            </div>'''
            return HttpResponse(html)
