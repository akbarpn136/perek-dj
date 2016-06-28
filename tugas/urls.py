from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^profil/$', views.index, name='halaman_profil'),
]
