# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-31 14:31
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_merge_20170329_1141'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='order',
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]