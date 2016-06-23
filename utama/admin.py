from django.contrib import admin
from .models import Kategori, Kegiatan, Format, Personil


# Register your models here.
admin.site.register(Kategori)
admin.site.register(Kegiatan)
admin.site.register(Format)
admin.site.register(Personil)
