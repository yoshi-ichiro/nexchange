# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-22 04:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_profile_smstoken'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='smstoken',
            new_name='sms_token',
        ),
    ]