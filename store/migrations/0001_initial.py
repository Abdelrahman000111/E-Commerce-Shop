# Generated by Django 5.0.1 on 2024-01-26 18:01

import django.db.models.deletion
import store.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0002_alter_category_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('price', models.FloatField(default=0)),
                ('description', models.TextField()),
                ('stock', models.IntegerField()),
                ('is_available', models.BooleanField(default=True)),
                ('image', models.ImageField(upload_to=store.models.image_product_upload)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.category')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
    ]
