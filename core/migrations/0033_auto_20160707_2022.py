# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-07 20:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_auto_20160707_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='tx_id',
            field=models.CharField(default=None, max_length=35, null=True),
        ),
    ]