from django.db import models

from utama.models import Kegiatan
from tugas.models import LembarKerja, LembarInstruksi


# Create your models here.
class Logbook(models.Model):
    nama = models.CharField(max_length=25, verbose_name='Jenis Tugas', default='Logbook')
    nomor = models.TextField(verbose_name='Nomor')
    tanggal = models.DateField(verbose_name='Tanggal')
    butir = models.CharField(max_length=20, verbose_name='Butir Kegiatan')
    angka = models.FloatField(verbose_name='Angka Kredit', default=0.0)
    uraian = models.TextField(verbose_name='Uraian Singkat', blank=True)
    isi = models.TextField(verbose_name='Isi')
    kegiatan = models.ForeignKey(Kegiatan, verbose_name='Kegiatan', on_delete=models.CASCADE)
    li = models.ForeignKey(LembarInstruksi, verbose_name='Lembar Instruksi', on_delete=models.CASCADE, default=1)
    pemberi = models.ForeignKey('auth.User', related_name='pemberi_tugas_lb', verbose_name='Pemberi Tugas',
                                on_delete=models.SET_NULL, null=True)
    penerima = models.ForeignKey('auth.User', related_name='penerima_tugas_lb', verbose_name='Penerima Tugas',
                                 on_delete=models.SET_NULL, null=True)
    pemeriksa = models.ForeignKey('auth.User', related_name='pemeriksa_tugas_lb', verbose_name='Pemeriksa Tugas',
                                  on_delete=models.SET_NULL, null=True)
    index = models.IntegerField(verbose_name='Index', default=0)
