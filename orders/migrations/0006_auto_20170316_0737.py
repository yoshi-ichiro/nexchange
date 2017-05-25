# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-16 07:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20170224_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_type',
            field=models.IntegerField(
                choices=[
                    (0,
                     'SELL'),
                    (1,
                     'BUY'),
                    (2,
                     'EXCHANGE')],
                default=1,
                help_text='BUY - Customer is giving fiat, and getting crypto money.<br/>SELL - Customer is giving crypto and getting fiat money<br/>EXCHANGE - Customer is exchanging different kinds of crypto currencies<br/>'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(
                choices=[
                    (-1,
                     'UNCONFIRMED PAYMENT'),
                    (0,
                     'CANCELED'),
                    (1,
                     'INITIAL'),
                    (2,
                     'PAID'),
                    (3,
                     'RELEASED'),
                    (4,
                     'COMPLETED')],
                default=1,
                help_text='INITIAL - Initial status of the order.<br/>PAID - Order is Paid by customer. Could be paid by crypto transaction or fiat payment, depending on order_type.<br/>PAID_UNCONFIRMED - Order is possibly paid (unconfirmed crypto transaction or fiat payment is to small to cover the order.)<br/>RELEASED - Order is paid by service provider. Could be paid by crypto transaction or fiat payment, depending on order_type.<br/>COMPLETED - All statuses of the order is completed<br/>CANCELED - Order is canceled.<br/>'),
        ),
    ]