# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-24 02:38
from __future__ import unicode_literals

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20160524_0140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='withdraw_address',
            field=models.CharField(
                max_length=35,
                validators=[
                    core.validators.validate_bc]),
        ),
    ]
