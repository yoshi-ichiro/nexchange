# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-28 13:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_auto_20170228_0844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cmspage',
            name='name',
            field=models.CharField(choices=[('about_us', 'about_us'), ('careers', 'careers'), ('press', 'press'), ('conference', 'conference'), ('legal_privacy', 'legal_privacy'), ('security', 'security'), ('faq', 'faq'), ('fees', 'fees'), ('support', 'support')], default=None, max_length=50),
        ),
        migrations.AlterField(
            model_name='ogresource',
            name='name',
            field=models.CharField(choices=[('about_us', 'about_us'), ('careers', 'careers'), ('press', 'press'), ('conference', 'conference'), ('legal_privacy', 'legal_privacy'), ('security', 'security'), ('faq', 'faq'), ('fees', 'fees'), ('support', 'support')], default=None, max_length=50),
        ),
    ]
