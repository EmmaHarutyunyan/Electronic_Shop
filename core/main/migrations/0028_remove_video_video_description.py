# Generated by Django 5.0.6 on 2024-07-27 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_alter_video_video_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='video_description',
        ),
    ]
