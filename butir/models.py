from django.db import models


awal = ''
PILIHAN_JENJANG = (
    (awal, '----'),
    ('Pertama', 'Perekayasa Pertama'),
    ('Muda', 'Perekayasa Muda'),
    ('Madya', 'Perekayasa Madya'),
    ('Utama', 'Perekayasa Utama'),
    ('Semua', 'Semua Jenjang'),
    ('Pertama/Muda', 'Pertama/Muda'),
    ('Muda/Madya', 'Muda/Madya'),
    ('Muda/Madya', 'Muda/Madya'),
    ('Madya/Muda', 'Madya/Muda'),
)


# Create your models here.
class ButirPendidikan(models.Model):
    butir = models.TextField(verbose_name='Butir Kegiatan')
    kodebutir = models.CharField(verbose_name='Kode Butir', max_length=50)
    hasil = models.CharField(verbose_name='Satuan Hasil', max_length=100)
    angka = models.FloatField(verbose_name='Angka Kredit')
    pelaksana = models.CharField(verbose_name='Pelaksana', max_length=20, choices=PILIHAN_JENJANG, default=awal)

    def __str__(self):
        return self.butir

    class Meta:
        verbose_name_plural = 'Butir Pendidikan'


class ButirPerekayasa(models.Model):
    butir = models.TextField(verbose_name='Butir Kegiatan')
    kodebutir = models.CharField(verbose_name='Kode Butir', max_length=50)
    hasil = models.CharField(verbose_name='Satuan Hasil', max_length=100)
    angka = models.FloatField(verbose_name='Angka Kredit', default=0.0)
    pelaksana = models.CharField(verbose_name='Pelaksana', max_length=20, choices=PILIHAN_JENJANG, default=awal)

    def __str__(self):
        return self.butir

    class Meta:
        verbose_name_plural = 'Butir Perekayasa'


class ButirProfesi(models.Model):
    butir = models.TextField(verbose_name='Butir Kegiatan')
    kodebutir = models.CharField(verbose_name='Kode Butir', max_length=50)
    hasil = models.CharField(verbose_name='Satuan Hasil', max_length=100)
    angka = models.FloatField(verbose_name='Angka Kredit', default=0.0)
    pelaksana = models.CharField(verbose_name='Pelaksana', max_length=20, choices=PILIHAN_JENJANG, default=awal)

    def __str__(self):
        return self.butir

    class Meta:
        verbose_name_plural = 'Butir Pengembangan Profesi'


class ButirPenunjang(models.Model):
    butir = models.TextField(verbose_name='Butir Kegiatan')
    kodebutir = models.CharField(verbose_name='Kode Butir', max_length=50)
    hasil = models.CharField(verbose_name='Satuan Hasil', max_length=100)
    angka = models.FloatField(verbose_name='Angka Kredit', default=0.0)
    pelaksana = models.CharField(verbose_name='Pelaksana', max_length=20, choices=PILIHAN_JENJANG, default=awal)

    def __str__(self):
        return self.butir

    class Meta:
        verbose_name_plural = 'Butir Penunjang'
