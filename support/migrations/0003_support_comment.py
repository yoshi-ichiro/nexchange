# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-23 14:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0002_auto_20170829_1033'),
    ]

    operations = [
        migrations.AddField(
            model_name='support',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
