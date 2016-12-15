# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-12-10 22:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20161128_0519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cmspage',
            name='name',
            field=models.CharField(
                choices=[
                    ('faq',
                     'faq'),
                    ('blog',
                     'blog'),
                    ('fees',
                     'fees'),
                    ('support',
                     'support'),
                    ('trading_guide',
                     'trading_guide'),
                    ('about_us',
                     'about_us'),
                    ('careers',
                     'careers'),
                    ('press',
                     'press'),
                    ('conference',
                     'conference'),
                    ('legal_privacy',
                     'legal_privacy'),
                    ('security',
                     'security')],
                default=None,
                max_length=50),
        ),
    ]
