# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-27 18:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verification', '0010_auto_20171201_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='verification',
            name='user_visible_comment',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]