from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default')
    is_superuser = models.BooleanField(default=False)
    joined_date = models.DateField(auto_now_add=True)
    level = models.PositiveIntegerField(default=1)
    xp = models.PositiveIntegerField(default=0)
    preferred_genres = models.ManyToManyField('books_database.Genre',
                                             related_name='prefered_genres')
    want_to_read_books = models.ManyToManyField('books_database.Book', related_name='want_to_read')
    currently_reading_books = models.ManyToManyField('books_database.Book',
                                                     related_name='currently_reading')
    def __str__(self):
        return self.username
