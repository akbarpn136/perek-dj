from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='halaman_utama'),
    url(r'^logout/$', views.keluar, name='halaman_logout'),

    url(r'^kategori/$', views.lihat_kategori, name='halaman_kategori'),
    url(r'^kategori/(?P<slug>[\w-]+)-(?P<pk>[0-9]+)/$', views.kegiatan_berdasarkan_kategori,
        name='halaman_kegiatan_kategori'),
    url(r'^cari/(?P<slug>[\w-]+)/$', views.cari_kegiatan, name='halaman_cari_kegiatan'),

    url(r'^json_kegiatan/$', views.bantu_kegiatan, name='json_kegiatan'),
]
