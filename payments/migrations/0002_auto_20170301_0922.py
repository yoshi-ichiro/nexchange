# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 09:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='payment',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='paymentcredentials',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='paymentpreference',
            managers=[
            ],
        ),
    ]