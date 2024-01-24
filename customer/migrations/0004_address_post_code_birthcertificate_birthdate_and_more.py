# Generated by Django 4.2.9 on 2024-01-24 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_remove_customerprofile_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='post_code',
            field=models.CharField(default='000000000', max_length=20),
        ),
        migrations.AddField(
            model_name='birthcertificate',
            name='birthdate',
            field=models.CharField(default='1300-01-01', max_length=10),
        ),
        migrations.AlterField(
            model_name='birthcertificate',
            name='birth_cert_number',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='customerprofile',
            name='emergency_mobile',
            field=models.CharField(max_length=20, null=True),
        ),
    ]