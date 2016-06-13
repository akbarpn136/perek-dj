from django.shortcuts import render, redirect
# from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import logout
# from django.contrib.auth.decorators import login_required

from .models import Kategori


# Create your views here.
def index(request, ol=None):
    data = {}
    if ol is None or ol == 'offline':
        return render(request, 'utama/halaman_utama.html', data)


def lihat_kategori(request):
    data_kategori = Kategori.objects.all()
    data = {
        'kategori': data_kategori
    }
    return render(request, 'utama/halaman_kategori.html', data)


def keluar(request):
    messages.info(request, 'Berhasil logout.')
    logout(request)

    return redirect('halaman_utama')
