# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-30 03:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tugas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lembarinstruksi',
            name='isi',
            field=models.TextField(default=None, verbose_name='Isi'),
        ),
        migrations.AddField(
            model_name='lembarkerja',
            name='isi',
            field=models.TextField(default=None, verbose_name='Isi'),
        ),
    ]
