# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-23 22:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('utama', '0004_auto_20160620_1327'),
    ]

    operations = [
        migrations.CreateModel(
            name='Personil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wbs_wp_pilihan', models.CharField(choices=[('', '----'), ('WBS', 'WBS'), ('WP', 'WP')], default='', max_length=3, verbose_name='WBS/WP')),
                ('wbs_wp_nama', models.CharField(max_length=180, verbose_name='Nama')),
                ('wbs_wp_kode', models.CharField(blank=True, max_length=10, verbose_name='Kode')),
                ('peran', models.CharField(choices=[('', '----'), ('ES', 'Engineering Staff'), ('L', 'Leader'), ('GL', 'Group Leader'), ('CE', 'Chief Engineering'), ('ACE', 'Assistant Chief Engineering'), ('PM', 'Program Manager'), ('PD', 'Program Director')], default='', max_length=3, verbose_name='Peran')),
                ('peran_kode', models.CharField(blank=True, max_length=10, verbose_name='Kode')),
                ('index', models.IntegerField(default=0, verbose_name='Index')),
                ('orang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Anggota')),
                ('personil_kegiatan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utama.Kegiatan', verbose_name='Kegiatan')),
            ],
            options={
                'ordering': ['index'],
            },
        ),
    ]
