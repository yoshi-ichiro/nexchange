# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-29 10:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verification', '0007_auto_20171128_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='verification',
            name='full_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
