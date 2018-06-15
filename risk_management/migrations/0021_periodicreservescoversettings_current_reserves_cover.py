# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-06-08 10:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('risk_management', '0020_auto_20180608_1003'),
    ]

    operations = [
        migrations.AddField(
            model_name='periodicreservescoversettings',
            name='current_reserves_cover',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='risk_management.ReservesCover'),
        ),
    ]