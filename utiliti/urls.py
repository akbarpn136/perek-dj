from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^profil/$', views.profil, name='halaman_profil'),
]
