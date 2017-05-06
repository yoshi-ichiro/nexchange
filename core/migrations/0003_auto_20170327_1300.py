# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 13:00
from __future__ import unicode_literals

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20170220_0130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address',
            field=models.CharField(
                max_length=42,
                validators=[
                    core.validators.validate_address]),
        ),
    ]
