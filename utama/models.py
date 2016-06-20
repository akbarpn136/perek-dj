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
    kapan_dibuat = models.DateField(verbose_name='Kapan dibuat')
    kode = models.CharField(max_length=200, verbose_name='Kode')
    referensi = models.TextField(verbose_name='Referensi')
    kategori_kegiatan = models.ManyToManyField(Kategori, verbose_name='Kategori', blank=True)

    def __str__(self):
        return self.nama

    class Meta:
        ordering = ['-kapan_dibuat']


class Format(models.Model):
    nama = models.CharField(max_length=150, verbose_name='Nama format')
    formasi = models.TextField(verbose_name='Kode dokumen')
    format_kegiatan = models.ForeignKey(Kegiatan, verbose_name='Kegiatan', on_delete=models.CASCADE)

    def __str__(self):
        return self.nama
