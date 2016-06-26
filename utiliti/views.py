from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages

from .models import Profil
from .forms import FormPersonil, FormUser


# Create your views here.
@login_required
def profil(request):
    try:
        data_profil = get_object_or_404(Profil, user=request.user.pk)
    except Http404:
        data_profil = Profil()

    try:
        data_user = get_object_or_404(User, pk=request.user.pk)

    except Http404:
        data_user = User()

    data = {
        'profil': data_profil,
        'user': data_user,
    }

    return render(request, 'utiliti/halaman_profil.html', data)


@login_required
def modifikasi_profil(request):
    try:
        data_user = get_object_or_404(User, pk=request.user.pk)

    except Http404:
        data_user = User()

    try:
        data_profil = get_object_or_404(Profil, user=request.user.pk)

    except Http404:
        data_profil = Profil()

    if request.method == 'POST':
        data_profil.user = data_user
        formulir = FormPersonil(request.POST, instance=data_profil)

        form_user = FormUser(request.POST, instance=data_user)

        if formulir.is_valid() and form_user.is_valid():
            messages.success(request, 'Data profil berhasil disimpan.')
            formulir.save()
            form_user.save()

            return redirect('halaman_profil')

    else:
        formulir = FormPersonil(instance=data_profil)
        form_user = FormUser(instance=data_user)

    data = {
        'profil': data_profil,
        'formulir': formulir,
        'formulir_user': form_user,
    }

    return render(request, 'utiliti/halaman_modif_profil.html', data)
