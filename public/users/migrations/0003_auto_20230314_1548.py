# Generated by Django 3.2.16 on 2023-03-14 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_mobile_number_tenantuser_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenantuser',
            name='national_id',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='tenantuser',
            name='phone_number',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
