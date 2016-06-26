from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^profil/$', views.profil, name='halaman_profil'),
    url(r'^profil/ubah$', views.modifikasi_profil, name='halaman_modifikasi_profil'),
]
