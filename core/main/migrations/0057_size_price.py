# Generated by Django 5.0.6 on 2024-08-18 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0056_remove_size_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='size',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
