# Generated by Django 5.1.4 on 2025-02-14 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books_database', '0020_rename_read_date_readbook_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookreview',
            old_name='review_date',
            new_name='date',
        ),
    ]
