# Generated by Django 4.2.9 on 2024-01-26 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_customerprofile_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerprofile',
            name='mobile',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
