# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-06 01:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tugas', '0004_auto_20160727_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='lembarinstruksi',
            name='kesepakatan',
            field=models.BooleanField(default=False, verbose_name='Setuju dihapus?'),
        ),
    ]
