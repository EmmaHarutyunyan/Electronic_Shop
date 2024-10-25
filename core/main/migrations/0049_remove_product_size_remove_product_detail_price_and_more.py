# Generated by Django 5.0.6 on 2024-08-14 19:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0048_product_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
        migrations.RemoveField(
            model_name='product_detail',
            name='price',
        ),
        migrations.RemoveField(
            model_name='product_detail',
            name='unit',
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.PositiveIntegerField(blank=True, null=True, verbose_name='Product size')),
                ('unit', models.CharField(blank=True, choices=[('GB', 'Gigabytes'), ('TB', 'Terabytes')], max_length=2, null=True, verbose_name='Size unit')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.product')),
            ],
        ),
        migrations.AlterField(
            model_name='product_detail',
            name='size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.size'),
        ),
    ]
