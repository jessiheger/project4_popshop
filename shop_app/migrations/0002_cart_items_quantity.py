# Generated by Django 2.0.5 on 2018-06-05 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart_items',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
