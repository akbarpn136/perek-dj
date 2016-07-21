from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/anggota/$', views.index, name='halaman_tugas_anggota'),
    url(r'^(?P<slug>[\w-]+)-(?P<pk>[0-9]+)-(?P<keg>[0-9]+)/rincian/$', views.lihat_li,
        name='halaman_tugas_anggota_rinci'),
]
