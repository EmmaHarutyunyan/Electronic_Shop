# Generated by Django 5.0.6 on 2024-08-12 13:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0039_color_alter_product_detail_color_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='color',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='colors', to='main.product'),
        ),
        migrations.AlterField(
            model_name='product_detail',
            name='color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='main.color'),
        ),
    ]
