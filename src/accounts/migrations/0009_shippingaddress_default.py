# Generated by Django 3.2 on 2023-03-22 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_shippingaddress_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='default',
            field=models.BooleanField(default=False),
        ),
    ]
