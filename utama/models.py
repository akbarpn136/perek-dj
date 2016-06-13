from django.db import models


# Create your models here.
class Kategori(models.Model):
    nama = models.CharField(max_length=200, verbose_name='Nama kategori')
    slug = models.SlugField(verbose_name='Slug')

    def __str__(self):
        return self.nama

    class Meta:
        ordering = ['nama']


class Kegiatan(models.Model):
    nama = models.CharField(max_length=255, verbose_name='Nama kegiatan')
    slug = models.SlugField(verbose_name='Slug')
    kapan_dibuat = models.DateField(verbose_name='Kapan dibuat', auto_now_add=True)
    kode = models.CharField(max_length=200, verbose_name='Kode')
    referensi = models.TextField(verbose_name='Referensi')
    kategori_kegiatan = models.ManyToManyField(Kategori, verbose_name='Kategori')

    def __str__(self):
        return self.nama

    class Meta:
        ordering = ['kapan_dibuat']
