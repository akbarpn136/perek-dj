from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='halaman_utama'),
    url(r'^logout/$', views.keluar, name='halaman_logout'),
]
