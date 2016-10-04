# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-04 14:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0071_auto_20161004_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cmspage',
            name='name',
            field=models.CharField(choices=[(('faq', 'FAQ'), ('faq', 'FAQ')), (('blog', 'Blog'), ('blog', 'Blog')), (('fees', 'Fees'), ('fees', 'Fees')), (('support', 'Support'), ('support', 'Support')), (('trading_guide', 'Trading Guide'), ('trading_guide', 'Trading Guide')), (('about_us', 'About Us'), ('about_us', 'About Us')), (('careers', 'Careers'), ('careers', 'Careers')), (('press', 'Press'), ('press', 'Press')), (('conference', 'Conference'), ('conference', 'Conference')), (('legal_privacy', 'Legal & Privacy'), ('legal_privacy', 'Legal & Privacy')), (('security', 'Security'), ('security', 'Security'))], default=None, max_length=50),
        ),
    ]
