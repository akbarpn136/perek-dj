from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='halaman_utama'),
    url(r'^kegiatan/tambah/$', views.tambah_kegiatan, name='halaman_tambah_kegiatan'),
    url(r'^kegiatan/(?P<slug>[\w-]+)-(?P<pk>[0-9]+)/ubah/$', views.ubah_kegiatan, name='halaman_ubah_kegiatan'),
    url(r'^kegiatan/(?P<slug>[\w-]+)-(?P<pk>[0-9]+)/hapus/$', views.hapus_kegiatan, name='halaman_hapus_kegiatan'),

    url(r'^kategori/$', views.lihat_kategori, name='halaman_kategori'),
    url(r'^kategori/(?P<slug>[\w-]+)-(?P<pk>[0-9]+)/$', views.kegiatan_berdasarkan_kategori,
        name='halaman_kegiatan_kategori'),
    url(r'^kategori/tambah/$', views.tambah_kategori, name='halaman_tambah_kategori'),
    url(r'^kategori/(?P<slug>[\w-]+)-(?P<pk>[0-9]+)/ubah/$', views.ubah_kategori, name='halaman_ubah_kategori'),
    url(r'^kategori/(?P<slug>[\w-]+)-(?P<pk>[0-9]+)/hapus/$', views.hapus_kategori, name='halaman_hapus_kategori'),

    url(r'^format/(?P<pk>[0-9]+)/$', views.lihat_format, name='halaman_format'),
    url(r'^format/tambah-(?P<pk>[0-9]+)/$', views.tambah_format, name='halaman_tambah_format'),
    url(r'^format/(?P<pk>[0-9]+)/ubah/(?P<keg_id>[0-9]+)$', views.ubah_format, name='halaman_ubah_format'),
    url(r'^format/(?P<pk>[0-9]+)/hapus/$', views.hapus_format, name='halaman_hapus_format'),

    url(r'^cari/(?P<slug>[\w-]+)/$', views.cari_kegiatan, name='halaman_cari_kegiatan'),
    url(r'^logout/$', views.keluar, name='halaman_logout'),

    url(r'^json_kegiatan/$', views.bantu_kegiatan, name='json_kegiatan'),
]
