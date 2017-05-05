# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-25 16:27
from __future__ import unicode_literals

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20170421_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address',
            field=models.CharField(max_length=42, unique=True, validators=[core.validators.validate_address]),
        ),
        migrations.AlterField(
            model_name='addressreserve',
            name='address',
            field=models.CharField(max_length=42, unique=True, verbose_name='address_id'),
        ),
        migrations.AlterField(
            model_name='addressreserve',
            name='card_id',
            field=models.CharField(blank=True, default=None, max_length=36, null=True, unique=True, verbose_name='card_id'),
        ),
    ]
