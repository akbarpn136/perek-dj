from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/lb@(?P<pk>[0-9]+).(?P<keg>[0-9]+).(?P<li>[0-9]+)/rincian/$', views.lihat_lb,
        name='halaman_lb_anggota_rinci'),

    url(r'^(?P<slug>[\w-]+)/cetak-(?P<pk>[0-9]+)-(?P<keg>[0-9]+)-lb/rincian@(?P<kode>[\w]+)/$', views.lihat_lb_rinci,
        name='halaman_lb_anggota_rinci_cetak'),

    url(r'^(?P<slug>[\w-]+)-(?P<keg>[0-9]+)/tambah.(?P<kode>[\w]+)@tugas=rincian-(?P<li>[0-9]+)/$', views.tambah_lb,
        name='halaman_tambah_lb_anggota'),
    url(r'^(?P<slug>[\w-]+)-(?P<keg>[0-9]+)/ubah.(?P<kode>[\w]+)-(?P<lb>[0-9]+)@tugas=rincian-(?P<li>[0-9]+)/$',
        views.ubah_lb, name='halaman_ubah_lb_anggota'),
    url(r'^(?P<slug>[\w-]+)-(?P<keg>[0-9]+)/duplikat.(?P<kode>[\w]+)-(?P<lb>[0-9]+)@tugas=rincian-(?P<li>[0-9]+)/$',
        views.duplikat_lb, name='halaman_duplikat_lb_anggota'),
    url(r'^hapus-(?P<pk>[0-9]+)/lb/$', views.hapus_lb, name='halaman_hapus_lb_anggota'),

    url(r'^(?P<cond>[\w.()]+)/butir/$', views.bantu_pilih_lb, name='halaman_bantu_pilih_lb'),
]
