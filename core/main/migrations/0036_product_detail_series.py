# Generated by Django 5.0.6 on 2024-08-11 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0035_remove_store_description_remove_store_discount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_detail',
            name='series',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
