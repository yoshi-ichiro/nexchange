# Generated by Django 2.0.7 on 2019-02-08 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0069_feediscount'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='rounding',
            field=models.IntegerField(default=8, help_text='Decimal places for order amount rounding.'),
        ),
        migrations.AlterField(
            model_name='currency',
            name='decimals',
            field=models.IntegerField(default=8, help_text='Decimal places used to convert satoshis to human readable decimal numbers.'),
        ),
    ]
