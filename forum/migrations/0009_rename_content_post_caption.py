# Generated by Django 5.1.4 on 2025-02-09 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0008_alter_post_content'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='content',
            new_name='caption',
        ),
    ]
