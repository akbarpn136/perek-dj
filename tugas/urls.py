from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/anggota/$', views.index, name='halaman_tugas_anggota'),
    url(r'^(?P<pk>[0-9]+)/anggota/(?P<usr>[\w.]+)$', views.index, name='halaman_tugas_anggota_filtered'),
    url(r'^(?P<slug>[\w-]+)/li-(?P<pk>[0-9]+)-(?P<keg>[0-9]+)/rincian/$', views.lihat_li,
        name='halaman_li_anggota_rinci'),
    url(r'^(?P<slug>[\w-]+)/lk-(?P<pk>[0-9]+)-(?P<keg>[0-9]+)/rincian-(?P<li>[0-9]+)/$', views.lihat_lk,
        name='halaman_lk_anggota_rinci'),
    url(r'^(?P<slug>[\w-]+)/cetak-(?P<pk>[0-9]+)-(?P<keg>[0-9]+)-li/rincian/$', views.lihat_li_rinci,
        name='halaman_li_anggota_rinci_cetak'),
    url(r'^(?P<slug>[\w-]+)/cetak-(?P<pk>[0-9]+)-(?P<keg>[0-9]+)-lk/rincian/$', views.lihat_lk_rinci,
        name='halaman_lk_anggota_rinci_cetak'),

    url(r'^(?P<usr>[\w.]+)/anggota/$', views.bantu_gravatar, name='json_bantu_gravatar'),
]
