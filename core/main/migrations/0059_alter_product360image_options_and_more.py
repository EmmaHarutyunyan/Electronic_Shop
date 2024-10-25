# Generated by Django 5.0.6 on 2024-08-25 18:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0058_product360image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product360image',
            options={},
        ),
        migrations.RemoveField(
            model_name='product360image',
            name='order',
        ),
        migrations.AlterField(
            model_name='product360image',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images_360', to='main.product'),
        ),
    ]
