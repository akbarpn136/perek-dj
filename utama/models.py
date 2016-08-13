from django.db import models


# Create your models here.
class Kategori(models.Model):
    nama = models.CharField(max_length=200, verbose_name='Nama kategori')
    slug = models.SlugField(verbose_name='Slug')

    def __str__(self):
        return self.nama

    class Meta:
        ordering = ['nama']
        verbose_name_plural = 'Kategori'


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
        verbose_name_plural = 'Kegiatan'


class Format(models.Model):
    default = ''
    PILIHAN = (
        ('TN', 'Technical Note'),
        ('TR', 'Technical Report'),
        ('TM', 'Technical Memorandum'),
        ('TD', 'Technical Document'),
        ('PCM', 'Progress Control and Monitoring'),
        ('IS', 'Instruction Sheet'),
        ('WS', 'Working Sheet'),
        ('LB', 'Logbook'),
        ('DS', 'Decision Sheet'),
    )

    nama = models.CharField(max_length=150, verbose_name='Nama format')
    formasi = models.TextField(verbose_name='Kode dokumen')
    format_kegiatan = models.ForeignKey(Kegiatan, verbose_name='Kegiatan', on_delete=models.CASCADE)
    kode = models.CharField(max_length=3, choices=PILIHAN, default=default, unique=True)

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name_plural = 'Format'


class Personil(models.Model):
    default = ''
    PILIHAN = (
        (default, '----'),
        ('WBS', 'WBS'),
        ('WP', 'WP'),
    )

    awal = ''
    PERAN = (
        (awal, '----'),
        ('TS', 'Technical Staff'),
        ('ES', 'Engineering Staff'),
        ('L', 'Leader'),
        ('GL', 'Group Leader'),
        ('CE', 'Chief Engineering'),
        ('ACE', 'Assistant Chief Engineering'),
        ('PM', 'Program Manager'),
        ('PD', 'Program Director'),
    )

    wbs_wp_pilihan = models.CharField(max_length=3, verbose_name='WBS/WP', choices=PILIHAN, default=default)
    wbs_wp_nama = models.CharField(max_length=180, verbose_name='Nama')
    wbs_wp_kode = models.CharField(max_length=10, verbose_name='Kode', blank=True)
    peran = models.CharField(max_length=3, verbose_name='Peran', choices=PERAN, default=awal)
    peran_kode = models.CharField(max_length=10, verbose_name='Kode', blank=True)
    peran_utama = models.BooleanField(verbose_name='Peran utama?', default=True)
    index = models.IntegerField(verbose_name='Index', default=0)

    orang = models.ForeignKey('auth.User', verbose_name='Anggota', on_delete=models.CASCADE)
    personil_kegiatan = models.ForeignKey(Kegiatan, verbose_name='Kegiatan', on_delete=models.CASCADE)

    def __str__(self):
        return self.peran + self.wbs_wp_nama + self.wbs_wp_kode + '.' + self.peran_kode

    def get_peran(self):
        pass

    class Meta:
        ordering = ['index']
        verbose_name_plural = 'Personil'
