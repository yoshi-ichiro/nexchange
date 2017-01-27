# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-12-27 10:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='support',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Email*'),
        ),
        migrations.AlterField(
            model_name='support',
            name='message',
            field=models.TextField(verbose_name='Message*'),
        ),
        migrations.AlterField(
            model_name='support',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Name*'),
        ),
    ]