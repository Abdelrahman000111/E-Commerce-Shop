# Generated by Django 5.0.1 on 2024-02-14 01:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_cart_item_has_offer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart_item',
            name='has_offer',
        ),
    ]
