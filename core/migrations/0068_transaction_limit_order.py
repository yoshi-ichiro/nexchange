# Generated by Django 2.0.7 on 2018-10-26 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0032_auto_20181026_1546'),
        ('core', '0067_currency_min_order_book_confirmations'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='limit_order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='transactions', to='orders.LimitOrder'),
        ),
    ]