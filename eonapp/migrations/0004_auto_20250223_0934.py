# Generated by Django 2.0.9 on 2025-02-23 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eonapp', '0003_cust_thoughtwaves_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller_order',
            name='orderstatus',
            field=models.CharField(max_length=200),
        ),
    ]
