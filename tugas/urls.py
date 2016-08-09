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

    url(r'^(?P<slug>[\w-]+)-(?P<keg>[0-9]+)/tambah.(?P<kode>[\w]+)/$', views.tambah_li,
        name='halaman_tambah_li_anggota'),
    url(r'^(?P<slug>[\w-]+)-(?P<keg>[0-9]+)/(?P<li>[\w]+).ubah.(?P<kode>[\w]+)/$', views.ubah_li,
        name='halaman_ubah_li_anggota'),
    url(r'^(?P<slug>[\w-]+)-(?P<keg>[0-9]+)/kesepakatan.(?P<li>[0-9]+)/$', views.kesepakatan_li,
        name='halaman_kesepakatan_li_anggota'),
    url(r'^hapus-(?P<pk>[0-9]+)/li/$', views.hapus_li, name='halaman_hapus_li_anggota'),

    url(r'^(?P<slug>[\w-]+)-(?P<keg>[0-9]+)/tambah.(?P<kode>[\w]+)@tugas=rincian-(?P<li>[0-9]+)/$', views.tambah_lk,
        name='halaman_tambah_lk_anggota'),
    url(r'^(?P<slug>[\w-]+)-(?P<keg>[0-9]+)/(?P<li>[\w]+).ubah.(?P<kode>[\w]+)/$', views.ubah_li,
        name='halaman_ubah_lk_anggota'),

    url(r'^(?P<usr>[\w.]+)/anggota/$', views.bantu_gravatar, name='json_bantu_gravatar'),
    url(r'^(?P<cond>[\w.()]+)/butir/(?P<keg>[0-9]+)/$', views.bantu_butir_perekayasa,
        name='json_bantu_butir_perekayasa'),
    url(r'^(?P<usr>[0-9]+)/peran/(?P<keg>[0-9]+)/$', views.bantu_peran, name='json_bantu_peran'),
]
