from django.shortcuts import get_object_or_404, Http404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import generic
from django.views.generic import edit
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from .models import LembarKeputusan
from utama.models import Kegiatan
from .forms import FormKeputusan


# Create your views here.
def cek_keanggotaan(user, pk_kegiatan):
    anggota_kegiatan = User.objects.filter(personil__personil_kegiatan=pk_kegiatan)
    return user.pk in anggota_kegiatan.values_list('pk', flat=True)


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
            data_keputusan = get_object_or_404(LembarKeputusan, pk=self.kwargs['pk_kegiatan'])
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
            return super(TambahKeputusan, self).dispatch(request, *args, **kwargs)
        else:
            messages.warning(request, 'Maaf, Anda tidak memiliki hak keanggotaan dari kegiatan ini.')
            return redirect('halaman_utama')

    def get_context_data(self, **kwargs):
        try:
            data_kegiatan = get_object_or_404(Kegiatan, pk=self.kwargs['pk'])
        except Http404:
            messages.warning(self.request, 'Halaman yang Anda cari tidak ditemukan')
            return redirect('halaman_utama')

        context = super(TambahKeputusan, self).get_context_data(**kwargs)
        context['peran'] = [self.request.user, data_kegiatan.pk]
        context['pk'] = data_kegiatan.pk
        context['kegiatan'] = data_kegiatan

        return context
