# Generated by Django 2.0.7 on 2018-11-21 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verification', '0025_verificationdocument_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='verificationdocument',
            name='contains_selfie',
            field=models.BooleanField(default=False),
        ),
    ]
