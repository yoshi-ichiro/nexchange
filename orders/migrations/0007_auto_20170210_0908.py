# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-10 09:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20170209_1322'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='moderator_flag',
        ),
        migrations.AlterField(
            model_name='order',
            name='unique_reference',
            field=models.CharField(max_length=5),
        ),
    ]
