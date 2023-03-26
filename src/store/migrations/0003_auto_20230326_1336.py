# Generated by Django 3.2 on 2023-03-26 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_stripe_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='nom')),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(default=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='store.category'),
        ),
    ]
