# Generated by Django 5.1.4 on 2025-01-04 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_user_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(default='profile_pictures/default.jpeg', upload_to='profile_pictures/'),
        ),
    ]
