# Generated by Django 5.0.6 on 2024-07-26 16:54

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_product_detail_color_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_detail',
            name='color',
            field=colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=25, samples=None, verbose_name='Product color'),
        ),
    ]