# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-09 13:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0014_auto_20170207_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='amount_cash',
            field=models.DecimalField(decimal_places=2, max_digits=14),
        ),
    ]