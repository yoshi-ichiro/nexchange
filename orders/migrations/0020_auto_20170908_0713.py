# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-08 07:13
from __future__ import unicode_literals

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0019_auto_20170906_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=django_fsm.FSMIntegerField(choices=[(12, 'UNCONFIRMED PAYMENT'), (14, 'PRE-RELEASE'), (0, 'CANCELED'), (11, 'INITIAL'), (13, 'PAID'), (15, 'RELEASED'), (16, 'COMPLETED')], default=11, help_text='INITIAL - Initial status of the order.<br/>PAID - Order is Paid by customer. Could be paid by crypto transaction or fiat payment, depending on order_type.<br/>PAID_UNCONFIRMED - Order is possibly paid (unconfirmed crypto transaction or fiat payment is to small to cover the order.)<br/>PRE_RELEASE - Order is prepared for RELEASE.<br/>RELEASED - Order is paid by service provider. Could be paid by crypto transaction or fiat payment, depending on order_type.<br/>COMPLETED - All statuses of the order is completed<br/>'),
        ),
    ]