# Generated by Django 5.0.6 on 2024-08-16 15:02

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0054_alter_cart_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_description',
            name='battery_life',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product_description',
            name='processor',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product_description',
            name='warranty',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='product_description',
            name='description',
            field=ckeditor.fields.RichTextField(verbose_name='Product description'),
        ),
    ]
