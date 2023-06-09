# Generated by Django 3.2 on 2023-03-22 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_shippingaddress_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopper',
            name='stripe_id',
            field=models.CharField(blank=True, max_length=90),
        ),
        migrations.AlterField(
            model_name='shopper',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='shopper',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
    ]
