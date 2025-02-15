from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default.jpg')
    is_superuser = models.BooleanField(default=False)
    joined_date = models.DateField(auto_now_add=True)
    preferred_genres = models.ManyToManyField('books_database.Genre',
                                             related_name='prefered_genres')
    def __str__(self):
        return self.username


class FollowRelation(models.Model):

    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed')
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Follow Relations'



