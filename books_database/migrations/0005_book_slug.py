# Generated by Django 5.1.4 on 2024-12-25 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_database', '0004_bookreview_readbook'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]