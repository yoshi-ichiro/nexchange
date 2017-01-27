# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-01-08 15:56
from __future__ import unicode_literals

from django.db import migrations, models

import core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_address_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address',
            field=models.CharField(
                max_length=42,
                validators=[
                    core.validators.validate_bc]),
        ),
    ]