# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-05-29 14:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('risk_management', '0019_auto_20180529_1407'),
        ('core', '0051_auto_20180514_0831'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='reserves_cover',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='risk_management.ReservesCover'),
        ),
        migrations.AlterField(
            model_name='address',
            name='type',
            field=models.CharField(choices=[('W', 'WITHDRAW'), ('D', 'DEPOSIT'), ('R', 'REFUND'), ('I', 'INTERNAL')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='orders.Order'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.CharField(choices=[('W', 'WITHDRAW'), ('D', 'DEPOSIT'), ('R', 'REFUND'), ('I', 'INTERNAL')], max_length=1, null=True),
        ),
    ]
