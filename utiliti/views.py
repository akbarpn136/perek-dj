from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Profil


# Create your views here.
@login_required
def profil(request):
    try:
        data_profil = get_object_or_404(Profil, user=request.user.pk)
    except Http404:
        data_profil = Profil()

    data = {
        'profil': data_profil,
    }

    return render(request, 'utiliti/halaman_profil.html', data)


@login_required
def modifikasi_profil(request):
    try:
        data_profil = get_object_or_404(Profil, user=request.user.pk)
    except Http404:
        data_profil = Profil()

    data = {
        'profil': data_profil,
    }

    return render(request, 'utiliti/halaman_profil.html', data)
