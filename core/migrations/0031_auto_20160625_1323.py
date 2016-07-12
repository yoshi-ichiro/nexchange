# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-25 13:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_auto_20160605_2332'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='address',
            name='order',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Order'),
        ),
        migrations.AddField(
            model_name='order',
            name='order_type',
            field=models.IntegerField(choices=[(0, 'SELL'), (1, 'BUY')], default=1),
        ),
        migrations.AddField(
            model_name='paymentmethod',
            name='bin',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='confirmations',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='transaction',
            name='tx_id',
            field=models.CharField(default=None, max_length=35),
        ),
        migrations.AlterField(
            model_name='payment',
            name='order',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Order'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='transaction', to='core.Order'),
        ),
    ]