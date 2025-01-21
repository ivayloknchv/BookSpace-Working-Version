from django.db import models
from users.models import User
from books_database.models import Book


class ActivityBase(models.Model):
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='initiator_%(class)s')
    activity_datetime =  models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class ActivityBook(ActivityBase):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_%(class)s')

    class Meta:
        abstract = True


class FollowActivity(ActivityBase):
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_user')

    class Meta:
        verbose_name_plural = "Follow Activities"


class WantToReadActivity(ActivityBook):
    pass

    class Meta:
        verbose_name_plural = "Want To Read Activities"


class CurrentlyReadingActivity(ActivityBook):
    pass

    class Meta:
        verbose_name_plural = "Currently Reading Activities"


class ReadActivity(ActivityBook):
    pass

    class Meta:
        verbose_name_plural = "Read Activities"


class RatingActivity(ActivityBook):
    stars = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Rating Activities"