# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-17 21:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_merge_20170406_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='ticker',
            field=models.CharField(
                blank=True,
                default=None,
                max_length=100,
                null=True),
        ),
        migrations.AddField(
            model_name='currency',
            name='wallet',
            field=models.CharField(
                blank=True,
                default=None,
                max_length=100,
                null=True),
        ),
    ]