# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-20 01:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('better_adds_count', models.IntegerField(default=0)),
                ('pair', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Pair')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Ticker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('ask', models.DecimalField(decimal_places=8, max_digits=18)),
                ('bid', models.DecimalField(decimal_places=8, max_digits=18)),
                ('pair', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Pair')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='price',
            name='ticker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ticker.Ticker'),
        ),
    ]
