# Generated by Django 5.1.4 on 2024-12-23 18:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books_database', '0002_rename_category_genre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='pages',
        ),
    ]
