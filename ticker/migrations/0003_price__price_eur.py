# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-19 22:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticker', '0002_auto_20160709_2333'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='_price_eur',
            field=models.FloatField(null=True),
        ),
    ]