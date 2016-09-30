# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-17 18:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0047_profile_disabled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='amount_btc',
            field=models.DecimalField(decimal_places=8, max_digits=10),
        ),
        migrations.AlterField(
            model_name='order',
            name='amount_cash',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount_cash',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]