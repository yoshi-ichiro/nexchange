# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-17 17:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20170108_1556'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FakeMigration',
        ),
    ]