# Generated by Django 5.0.6 on 2024-07-27 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='video_url',
        ),
        migrations.AddField(
            model_name='video',
            name='video_file',
            field=models.FileField(null=True, upload_to='videos/'),
        ),
    ]