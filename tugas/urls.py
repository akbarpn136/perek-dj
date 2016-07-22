from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/anggota/$', views.index, name='halaman_tugas_anggota'),
    url(r'^(?P<pk>[0-9]+)/anggota/(?P<usr>[\w.]+)$', views.index, name='halaman_tugas_anggota_filtered'),
    url(r'^(?P<slug>[\w-]+)-(?P<pk>[0-9]+)-(?P<keg>[0-9]+)/rincian/$', views.lihat_li,
        name='halaman_tugas_anggota_rinci'),

    url(r'^(?P<usr>[\w.]+)/anggota/$', views.bantu_gravatar, name='json_bantu_gravatar'),
]
