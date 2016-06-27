from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages

from .models import Profil
from .forms import FormPersonil, FormUser, FormGantiSandi


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


@login_required
def ganti_password(request):
    try:
        u = get_object_or_404(User, username=request.user.username)
    except Http404:
        messages.warning(request, 'Maaf, user tidak ditemukan')
        return redirect('halaman_profil')

    if request.method == 'POST':
        sandi_lama = request.POST.get('password_lama')
        sandi_baru = request.POST.get('password_baru')
        sandi_konfirm = request.POST.get('password_konfirm')

        user = authenticate(username=request.user.username, password=sandi_lama)

        formulir = FormGantiSandi(request.POST)
        if formulir.is_valid():
            if user is not None:
                if sandi_baru == sandi_konfirm:
                    u.set_password(sandi_baru)
                    u.save()

                    messages.success(request, 'Password baru berhasil disimpan')
                    return redirect('halaman_utama')
                else:
                    messages.warning(request, 'Gagal konfirmasi password!')
            else:
                messages.warning(request, 'Password lama tidak ditemukan!')

    else:
        formulir = FormGantiSandi()

    data = {
        'formulir': formulir
    }

    return render(request, 'registration/halaman_ganti_sandi.html', data)
