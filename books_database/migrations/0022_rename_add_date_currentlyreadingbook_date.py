# Generated by Django 5.1.4 on 2025-02-14 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books_database', '0021_rename_review_date_bookreview_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='currentlyreadingbook',
            old_name='add_date',
            new_name='date',
        ),
    ]
