from django.db import models

from utama.models import Kegiatan


# Create your models here.
class LembarInstruksi(models.Model):
    nama = models.CharField(max_length=25, verbose_name='Jenis Tugas', default='Lembar Instruksi')
    nomor = models.TextField(verbose_name='Nomor')
    referensi = models.TextField(verbose_name='Referensi')
    tanggal = models.DateField(verbose_name='Tanggal')
    butir = models.CharField(max_length=20, verbose_name='Butir Kegiatan')
    kegiatan = models.ForeignKey(Kegiatan, verbose_name='Kegiatan', on_delete=models.CASCADE)
    pemberi = models.ForeignKey('auth.User', related_name='pemberi_tugas', verbose_name='Pemberi Tugas',
                                on_delete=models.SET_NULL, null=True)
    penerima = models.ForeignKey('auth.User', related_name='penerima_tugas', verbose_name='Penerima Tugas',
                                 on_delete=models.SET_NULL, null=True)
    index = models.IntegerField(verbose_name='Index', default=0)

    def __str__(self):
        return self.nama + ' ' + self.nomor

    class Meta:
        verbose_name_plural = 'Lembar Instruksi'


class LembarKerja(models.Model):
    nama = models.CharField(max_length=25, verbose_name='Jenis Tugas', default='Lembar Kerja')
    nomor = models.TextField(verbose_name='Nomor')
    referensi = models.TextField(verbose_name='Referensi')
    tanggal = models.DateField(verbose_name='Tanggal')
    butir = models.CharField(max_length=20, verbose_name='Butir Kegiatan')
    kegiatan = models.ForeignKey(Kegiatan, verbose_name='Kegiatan', on_delete=models.CASCADE)
    pemberi = models.ForeignKey('auth.User', related_name='pemberi_tugas_lk', verbose_name='Pemberi Tugas',
                                on_delete=models.SET_NULL, null=True)
    penerima = models.ForeignKey('auth.User', related_name='penerima_tugas_lk', verbose_name='Penerima Tugas',
                                 on_delete=models.SET_NULL, null=True)
    index = models.IntegerField(verbose_name='Index', default=0)

    def __str__(self):
        return self.nama + ' ' + self.nomor

    class Meta:
        verbose_name_plural = 'Lembar Kerja'
