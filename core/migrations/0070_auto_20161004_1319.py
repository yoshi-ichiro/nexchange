# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-04 13:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0069_auto_20161004_1314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seofooter',
            name='type',
        ),
        migrations.AlterField(
            model_name='seofooter',
            name='locale',
            field=models.CharField(
                choices=[
                    ('ru',
                     'Russian'),
                    ('en',
                     'English')],
                default=(
                    'ru',
                    'Russian'),
                max_length=2,
                null=True),
        ),
        migrations.AlterField(
            model_name='seofooter',
            name='name',
            field=models.CharField(
                choices=[
                    ('About Us',
                     'About Us'),
                    ('Careers',
                     'Careers'),
                    ('Press',
                     'Press'),
                    ('Conference',
                     'Conference'),
                    ('Legal & Privacy',
                     'Legal & Privacy'),
                    ('Security',
                     'Security'),
                    ('FAQ',
                     'FAQ'),
                    ('Blog',
                     'Blog'),
                    ('Fees',
                     'Fees'),
                    ('Support',
                     'Support'),
                    ('Trading Guide',
                     'Trading Guide')],
                default=None,
                max_length=50),
        ),
    ]
