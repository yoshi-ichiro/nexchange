# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-20 22:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20170420_2231'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='median_confirmation',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]