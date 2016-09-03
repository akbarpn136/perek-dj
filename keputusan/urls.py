from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<slug>[\w-]+)-(?P<pk>[0-9]+)/rincian/$', views.LihatKeputusan.as_view(), name='halaman_keputusan'),
    url(r'^(?P<slug>[\w-]+)-(?P<pk_kegiatan>[0-9]+)-(?P<pk>[0-9]+)/rincian$', views.RincianKeputusan.as_view(),
        name='halaman_rincian_keputusan'),
    url(r'^(?P<slug>[\w-]+)-(?P<pk>[0-9]+)/tambah/$', views.TambahKeputusan.as_view(),
        name='halaman_tambah_keputusan'),
    url(r'^(?P<slug>[\w-]+)-(?P<pk_kegiatan>[0-9]+)-(?P<pk>[0-9]+)/ubah', views.UbahKeputusan.as_view(),
        name='halaman_ubah_keputusan'),
    url(r'^(?P<slug>[\w-]+)-(?P<pk_kegiatan>[0-9]+)-(?P<pk>[0-9]+)/hapus', views.HapusKeputusan.as_view(),
        name='halaman_hapus_keputusan'),
    url(r'^(?P<slug>[\w-]+)-(?P<pk_kegiatan>[0-9]+)-(?P<pk>[0-9]+)/duplikat', views.DuplikatKeputusan.as_view(),
        name='halaman_duplikat_keputusan'),

    url(r'^(?P<cond>[\w.()]+)/butir/(?P<keg>[0-9]+)/$', views.bantu_butir_perekayasa,
        name='json_bantu_butir_perekayasa'),
]
