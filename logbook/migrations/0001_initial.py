# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-13 04:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('utama', '0009_format_kode'),
        ('tugas', '0006_auto_20160813_1106'),
    ]

    operations = [
        migrations.CreateModel(
            name='Logbook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(default='Logbook', max_length=25, verbose_name='Jenis Tugas')),
                ('nomor', models.TextField(verbose_name='Nomor')),
                ('tanggal', models.DateField(verbose_name='Tanggal')),
                ('butir', models.CharField(max_length=20, verbose_name='Butir Kegiatan')),
                ('angka', models.FloatField(default=0.0, verbose_name='Angka Kredit')),
                ('uraian', models.TextField(blank=True, verbose_name='Uraian Singkat')),
                ('isi', models.TextField(verbose_name='Isi')),
                ('index', models.IntegerField(default=0, verbose_name='Index')),
                ('kegiatan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utama.Kegiatan', verbose_name='Kegiatan')),
                ('pemberi', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pemberi_tugas_lb', to=settings.AUTH_USER_MODEL, verbose_name='Pemberi Tugas')),
                ('pemeriksa', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pemeriksa_tugas_lb', to=settings.AUTH_USER_MODEL, verbose_name='Pemeriksa Tugas')),
                ('penerima', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='penerima_tugas_lb', to=settings.AUTH_USER_MODEL, verbose_name='Penerima Tugas')),
                ('referensi', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tugas.LembarKerja', verbose_name='Referensi')),
            ],
        ),
    ]
