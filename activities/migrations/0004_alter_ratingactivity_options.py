# Generated by Django 5.1.4 on 2025-01-21 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0003_alter_currentlyreadingactivity_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ratingactivity',
            options={'verbose_name_plural': 'Rating Activities'},
        ),
    ]