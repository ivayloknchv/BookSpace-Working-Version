# Generated by Django 5.1.4 on 2025-02-14 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_database', '0016_alter_wanttoreadbook_add_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wanttoreadbook',
            name='add_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
