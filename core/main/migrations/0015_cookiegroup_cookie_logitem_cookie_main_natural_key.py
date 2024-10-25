# Generated by Django 5.0.6 on 2024-07-08 16:46

import django.core.validators
import django.db.models.deletion
import re
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_cookieconsent'),
    ]

    operations = [
        migrations.CreateModel(
            name='CookieGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('varname', models.CharField(max_length=32, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[-_a-zA-Z0-9]+$'), "Enter a valid 'varname' consisting of letters, numbers, underscores or hyphens.", 'invalid')], verbose_name='Variable name')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('is_required', models.BooleanField(default=False, help_text='Are cookies in this group required.', verbose_name='Is required')),
                ('is_deletable', models.BooleanField(default=True, help_text='Can cookies in this group be deleted.', verbose_name='Is deletable?')),
                ('ordering', models.IntegerField(default=0, verbose_name='Ordering')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
            ],
            options={
                'verbose_name': 'Cookie Group',
                'verbose_name_plural': 'Cookie Groups',
                'ordering': ['ordering'],
            },
        ),
        migrations.CreateModel(
            name='Cookie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('path', models.TextField(blank=True, default='/', verbose_name='Path')),
                ('domain', models.CharField(blank=True, max_length=250, verbose_name='Domain')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('cookiegroup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.cookiegroup', verbose_name='Cookie Group')),
            ],
            options={
                'verbose_name': 'Cookie',
                'verbose_name_plural': 'Cookies',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='LogItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.IntegerField(choices=[(-1, 'Declined'), (1, 'Accepted')], verbose_name='Action')),
                ('version', models.CharField(max_length=32, verbose_name='Version')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('cookiegroup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.cookiegroup', verbose_name='Cookie Group')),
            ],
            options={
                'verbose_name': 'Log item',
                'verbose_name_plural': 'Log items',
                'ordering': ['-created'],
            },
        ),
        migrations.AddConstraint(
            model_name='cookie',
            constraint=models.UniqueConstraint(fields=('name', 'description'), name='main_natural_key'),
        ),
    ]