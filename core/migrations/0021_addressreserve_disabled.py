# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-07 13:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_pair_disable_ticker'),
    ]

    operations = [
        migrations.AddField(
            model_name='addressreserve',
            name='disabled',
            field=models.BooleanField(default=False),
        ),
    ]
