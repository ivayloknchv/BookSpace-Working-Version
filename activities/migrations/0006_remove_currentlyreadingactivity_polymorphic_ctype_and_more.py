# Generated by Django 5.1.4 on 2025-02-04 21:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0005_currentlyreadingactivity_polymorphic_ctype_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='currentlyreadingactivity',
            name='polymorphic_ctype',
        ),
        migrations.RemoveField(
            model_name='followactivity',
            name='polymorphic_ctype',
        ),
        migrations.RemoveField(
            model_name='ratingactivity',
            name='polymorphic_ctype',
        ),
        migrations.RemoveField(
            model_name='readactivity',
            name='polymorphic_ctype',
        ),
        migrations.RemoveField(
            model_name='wanttoreadactivity',
            name='polymorphic_ctype',
        ),
    ]
