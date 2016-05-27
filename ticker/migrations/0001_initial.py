# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-26 16:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[('B', 'BUY'), ('S', 'SELL')], max_length=1)),
                ('price_rub', models.FloatField()),
                ('price_usd', models.FloatField()),
                ('rate', models.FloatField()),
                ('better_adds_count', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]