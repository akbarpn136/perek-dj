from django.db import models


# Create your models here.
class Profil(models.Model):
    awal = ''
    PILIHAN_JENJANG = (
        (awal, '----'),
        ('Pertama', 'Perekayasa Pertama'),
        ('Muda', 'Perekayasa Muda'),
        ('Madya', 'Perekayasa Madya'),
        ('Utama', 'Perekayasa Utama'),
    )

    nip = models.CharField(max_length=50, verbose_name='NIP')
    pendidikan = models.CharField(max_length=150, verbose_name='Pendidikan')
    instansi = models.TextField(verbose_name='Nama Lengkap Unit')
    instansi_kode = models.CharField(max_length=20, verbose_name='Singkatan Unit')
    satuan = models.TextField(verbose_name='Nama Lengkap Satuan kerja', blank=True)
    kantor = models.TextField(verbose_name='Nama Lengkap Kantor', blank=True)
    pangkat = models.TextField(verbose_name='Pangkat/Golongan Ruang/TMT')
    jabatan = models.CharField(max_length=150, verbose_name='Jabatan')
    jenjang = models.CharField(max_length=10, verbose_name='Jenjang Perekayasa', choices=PILIHAN_JENJANG, default=awal)
    user = models.ForeignKey('auth.User', verbose_name='Personil', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Profil'

    def __str__(self):
        return self.nip
