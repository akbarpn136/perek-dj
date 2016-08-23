# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-19 04:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utiliti', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profil',
            name='kantor',
            field=models.TextField(blank=True, verbose_name='Nama Lengkap Kantor'),
        ),
        migrations.AddField(
            model_name='profil',
            name='satuan',
            field=models.TextField(blank=True, verbose_name='Nama Lengkap Satuan kerja'),
        ),
        migrations.AlterField(
            model_name='profil',
            name='instansi',
            field=models.TextField(verbose_name='Nama Lengkap Unit'),
        ),
        migrations.AlterField(
            model_name='profil',
            name='instansi_kode',
            field=models.CharField(max_length=20, verbose_name='Singkatan Unit'),
        ),
    ]