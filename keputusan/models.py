from django.db import models

from utama.models import Kegiatan


# Create your models here.
class LembarKeputusan(models.Model):
    nama = models.CharField(max_length=25, verbose_name='Jenis Tugas', default='Lembar Keputusan')
    nomor = models.TextField(verbose_name='Nomor')
    tanggal = models.DateField(verbose_name='Tanggal')
    tingkatan = models.CharField(max_length=20, verbose_name='Tingkatan Rapat')
    angka = models.FloatField(verbose_name='Angka Kredit')
    uraian = models.TextField(verbose_name='Uraian Singkat', blank=True)
    isi = models.TextField(verbose_name='Isi')
    kegiatan = models.ForeignKey(Kegiatan, verbose_name='Kegiatan', on_delete=models.CASCADE)
    index = models.IntegerField(verbose_name='Index', default=0)
    pemberi = models.ForeignKey('auth.User', verbose_name='Pimpinan rapat', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nama + ' ' + self.nomor

    class Meta:
        verbose_name_plural = 'Lembar Keputusan'
