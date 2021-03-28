# Generated by Django 3.1.7 on 2021-03-28 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='product_remaining',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='products',
            name='product_price',
            field=models.FloatField(default=0.0),
        ),
    ]