from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<slug>[\w-]+)-(?P<pk>[0-9]+)/rincian/$', views.LihatKeputusan.as_view(), name='halaman_keputusan'),
    url(r'^(?P<slug>[\w-]+)-(?P<pk_kegiatan>[0-9]+)-(?P<pk>[0-9]+)/rincian$', views.RincianKeputusan.as_view(),
        name='halaman_rincian_keputusan'),
    url(r'^(?P<slug>[\w-]+)-(?P<pk>[0-9]+)/tambah/$', views.TambahKeputusan.as_view(),
        name='halaman_tambah_keputusan'),

    # url(r'^(?P<slug>[\w-]+)/cetak-(?P<pk>[0-9]+)-(?P<keg>[0-9]+)-lb/rincian@(?P<kode>[\w]+)/$', views.lihat_lb_rinci,name='halaman_lb_anggota_rinci_cetak'),

    # url(r'^(?P<slug>[\w-]+)-(?P<keg>[0-9]+)/tambah.(?P<kode>[\w]+)@tugas=rincian-(?P<li>[0-9]+)/$', views.tambah_lb,name='halaman_tambah_lb_anggota'),
    # url(r'^(?P<slug>[\w-]+)-(?P<keg>[0-9]+)/ubah.(?P<kode>[\w]+)-(?P<lb>[0-9]+)@tugas=rincian-(?P<li>[0-9]+)/$',views.ubah_lb, name='halaman_ubah_lb_anggota'),
    # url(r'^(?P<slug>[\w-]+)-(?P<keg>[0-9]+)/duplikat.(?P<kode>[\w]+)-(?P<lb>[0-9]+)@tugas=rincian-(?P<li>[0-9]+)/$',views.duplikat_lb, name='halaman_duplikat_lb_anggota'),
    # url(r'^hapus-(?P<pk>[0-9]+)/lb/$', views.hapus_lb, name='halaman_hapus_lb_anggota'),
    url(r'^(?P<cond>[\w.()]+)/butir/(?P<keg>[0-9]+)/$', views.bantu_butir_perekayasa,
        name='json_bantu_butir_perekayasa'),
]
