# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-15 13:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_auto_20170331_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_preference',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='payments.PaymentPreference'),
        ),
        migrations.AlterField(
            model_name='order',
            name='unique_reference',
            field=models.CharField(blank=True, max_length=16),
        ),
        migrations.AlterField(
            model_name='order',
            name='withdraw_address',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_set', to='core.Address'),
        ),
    ]