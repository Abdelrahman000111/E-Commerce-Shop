# Generated by Django 5.0.1 on 2024-02-29 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_remove_cart_item_variation_cart_item_variation_color_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart_item',
            name='variation_color',
        ),
        migrations.RemoveField(
            model_name='cart_item',
            name='variation_size',
        ),
    ]
