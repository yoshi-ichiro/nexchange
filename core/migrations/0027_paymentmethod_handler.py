# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-31 18:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_remove_paymentmethod_handler'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmethod',
            name='handler',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
