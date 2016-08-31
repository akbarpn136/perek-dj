from django.shortcuts import render, get_object_or_404, Http404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView


from .models import LembarKeputusan
from utama.models import Kegiatan


# Create your views here.
def cek_keanggotaan(user, pk_kegiatan):
    anggota_kegiatan = User.objects.filter(personil__personil_kegiatan=pk_kegiatan)
    return user.pk in anggota_kegiatan.values_list('pk', flat=True)


class LihatKeputusan(ListView):
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
