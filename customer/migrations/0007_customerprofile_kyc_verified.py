# Generated by Django 4.2.9 on 2024-01-26 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_alter_customerprofile_mobile'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerprofile',
            name='kyc_verified',
            field=models.BooleanField(default=False),
        ),
    ]
