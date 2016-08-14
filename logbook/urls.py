from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^(?P<slug>[\w-]+)/lk-(?P<pk>[0-9]+)-(?P<keg>[0-9]+)/rincian-(?P<li>[0-9]+)/$', views.lihat_lk, name='halaman_lk_anggota_rinci'),

    # url(r'^(?P<slug>[\w-]+)/cetak-(?P<pk>[0-9]+)-(?P<keg>[0-9]+)-lk/rincian/$', views.lihat_lk_rinci, name='halaman_lk_anggota_rinci_cetak'),

    url(r'^(?P<slug>[\w-]+)-(?P<keg>[0-9]+)/tambah.(?P<kode>[\w]+)@tugas=rincian-(?P<li>[0-9]+)/$', views.tambah_lb,
        name='halaman_tambah_lb_anggota'),
    # url(r'^(?P<slug>[\w-]+)-(?P<keg>[0-9]+)/ubah.(?P<kode>[\w]+)-(?P<lk>[0-9]+)@tugas=rincian-(?P<li>[0-9]+)/$', views.ubah_lk, name='halaman_ubah_lk_anggota'),
    # url(r'^(?P<slug>[\w-]+)-(?P<keg>[0-9]+)/duplikat.(?P<kode>[\w]+)-(?P<lk>[0-9]+)@tugas=rincian-(?P<li>[0-9]+)/$', views.duplikat_lk, name='halaman_duplikat_lk_anggota'),
    # url(r'^hapus-(?P<pk>[0-9]+)/lk/$', views.hapus_lk, name='halaman_hapus_lk_anggota'),
]
