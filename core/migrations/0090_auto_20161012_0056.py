# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-12 00:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0089_auto_20161012_0000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cmspage',
            name='name',
            field=models.CharField(
                choices=[
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
                     'security'),
                    ('faq',
                     'faq'),
                    ('blog',
                     'blog'),
                    ('fees',
                     'fees'),
                    ('support',
                     'support'),
                    ('trading_guide',
                     'trading_guide')],
                default=None,
                max_length=50),
        ),
    ]