from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/anggota/$', views.index, name='halaman_tugas_anggota'),
]
