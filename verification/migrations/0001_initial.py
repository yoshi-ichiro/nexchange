# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-12 10:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import verification.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Verification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False)),
                ('disabled', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('identity_document', models.ImageField(upload_to=verification.models.Verification.identity_file_name)),
                ('utility_document', models.ImageField(upload_to=verification.models.Verification._utility_file_name)),
                ('id_status', models.CharField(blank=True, choices=[('REJECTED', 'Rejected'), ('OK', 'Approved')], max_length=10, null=True)),
                ('util_status', models.CharField(blank=True, choices=[('REJECTED', 'Rejected'), ('OK', 'Approved')], max_length=10, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
