# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-08 21:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticker', '0002_auto_20160708_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='price',
            name='modified_on',
            field=models.DateTimeField(auto_now=True, default=None),
            preserve_default=False,
        ),
    ]
