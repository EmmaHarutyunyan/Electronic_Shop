# Generated by Django 5.0.6 on 2024-07-27 18:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_remove_video_video_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='all_products',
            name='slide',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.slide'),
        ),
    ]
