# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-12-12 15:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0017_auto_20161212_1530'),
        ('payments', '0004_auto_20161212_1530'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False)),
                ('disabled', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('order_type', models.IntegerField(choices=[(0, 'SELL'), (1, 'BUY')], default=1)),
                ('amount_cash', models.DecimalField(decimal_places=2, max_digits=12)),
                ('amount_btc', models.DecimalField(decimal_places=8, max_digits=18)),
                ('payment_window', models.IntegerField(default=60)),
                ('is_paid', models.BooleanField(default=False)),
                ('is_released', models.BooleanField(default=False)),
                ('is_completed', models.BooleanField(default=False)),
                ('is_failed', models.BooleanField(default=False)),
                ('unique_reference', models.CharField(max_length=5, unique=True)),
                ('admin_comment', models.CharField(max_length=200)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Currency')),
                ('payment_preference', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='payments.PaymentPreference')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_on'],
            },
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
