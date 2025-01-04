# Generated by Django 5.1.4 on 2024-12-24 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_database', '0004_bookreview_readbook'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='read_books',
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='prefered_genres',
            field=models.ManyToManyField(related_name='prefered_genres', to='books_database.genre'),
        ),
    ]