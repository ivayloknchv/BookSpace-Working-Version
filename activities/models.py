from django.db import models
from django.utils.safestring import mark_safe
from books_database.models import Book
from django.urls import reverse


class ActivityBase(models.Model):

    initiator = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='initiator_%(class)s')

    class Meta:
        abstract = True

    def display_activity(self):
        pass


class ActivityBook(ActivityBase):

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_%(class)s')

    class Meta:
        abstract = True


class ForumActivity(ActivityBase):
    thread = models.ForeignKey('forum.Thread', on_delete=models.CASCADE, related_name='thread_%(class)s')

    class Meta:
        abstract = True


class FollowActivity(ActivityBase):

    followed_user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='followed_user')

    class Meta:
        verbose_name_plural = "Follow Activities"

    def display_activity(self):
        initiator_url = reverse('profile', args=[self.initiator.username])
        followed_url = reverse('profile', args=[self.followed_user.username])
        result_str =  (f'<b><a href = "{initiator_url}">{self.initiator}</a></b> followed '
                       f'<b><a href = "{followed_url}">{self.followed_user}</a></b><br><br>')
        return result_str

    def __str__(self):
        return f'{self.initiator} followed {self.followed_user}'


class NewThreadActivity(ForumActivity):

    class Meta:
        verbose_name_plural = "New Thread Activities"

    def display_activity(self):
        initiator_url = reverse('profile', args=[self.initiator.username])
        thread_url = reverse('view_thread', args=[self.thread.slug])
        result_str = (f'<b><a href = "{initiator_url}">{self.initiator}</a></b> created a '
                      f'new thread <b><a href = "{thread_url}">{self.thread}</a></b><br><br>')
        return result_str

    def __str__(self):
        return f'{self.initiator} created a new thread {self.thread}'


class NewPostActivity(ForumActivity):

    class Meta:
        verbose_name_plural = "New Post Activities"

    def display_activity(self):
        initiator_url = reverse('profile', args=[self.initiator.username])
        thread_url = reverse('view_thread', args=[self.thread.slug])
        result_str = (f'<b><a href = "{initiator_url}">{self.initiator}</a></b> posted in '
                      f'<b><a href = "{thread_url}">{self.thread}</a></b><br><br>')
        return result_str

    def __str__(self):
        return f'{self.initiator} posted in {self.thread}'


class WantToReadActivity(ActivityBook):

    class Meta:
        verbose_name_plural = "Want To Read Activities"

    def display_activity(self):
        initiator_url = reverse('profile', args=[self.initiator.username])
        book_url = reverse('book', args=[self.book.slug])
        result_str = (f'<b><a href = "{initiator_url}">{self.initiator}</a></b> wants to read '
                               f'<b><a href = "{book_url}">{self.book}</a></b><br><br>')
        return result_str

    def __str__(self):
        return f'{self.initiator} wants to read {self.book}'


class CurrentlyReadingActivity(ActivityBook):

    class Meta:
        verbose_name_plural = "Currently Reading Activities"

    def display_activity(self):
        initiator_url = reverse('profile', args=[self.initiator.username])
        book_url = reverse('book', args=[self.book.slug])
        result_str = (f'<b><a href = "{initiator_url}">{self.initiator}</a></b> is currently reading '
                       f'<b><a href = "{book_url}">{self.book}</a></b><br><br>')
        return result_str

    def __str__(self):
        return f'{self.initiator} is currently reading {self.book}'


class ReadActivity(ActivityBook):

    class Meta:
        verbose_name_plural = "Read Activities"

    def display_activity(self):
        initiator_url = reverse('profile', args=[self.initiator.username])
        book_url = reverse('book', args=[self.book.slug])
        result_str = (f'<b><a href = "{initiator_url}">{self.initiator}</a></b> read '
                      f'<b><a href = "{book_url}">{self.book}</a></b><br><br>')
        return result_str

    def __str__(self):
        return f'{self.initiator} read {self.book}'


class RatingActivity(ActivityBook):
    stars = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Rating Activities"

    def display_activity(self):
        initiator_url = reverse('profile', args=[self.initiator.username])
        book_url = reverse('book', args=[self.book.slug])
        result_str = (f'<b><a href = "{initiator_url}">{self.initiator}</a></b> rated '
                      f'<b><a href = "{book_url}">{self.book}</a></b> with <b>{self.stars}</b> stars.<br><br>')
        return result_str

    def __str__(self):
        return f'{self.initiator} rated {self.book} with {self.stars}'


class ActivityWrapper(models.Model):
    initiator = models.ForeignKey('users.User', on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    follow_activity = models.ForeignKey(FollowActivity, on_delete=models.CASCADE, null=True, blank=True)
    new_thread_activity = models.ForeignKey(NewThreadActivity, on_delete=models.CASCADE, null=True, blank=True)
    want_to_read_activity = models.ForeignKey(WantToReadActivity, on_delete=models.CASCADE, null=True, blank=True)
    new_post_activity = models.ForeignKey(NewPostActivity, on_delete=models.CASCADE, null=True, blank=True)
    currently_reading_activity = models.ForeignKey(CurrentlyReadingActivity, on_delete=models.CASCADE, null=True, blank=True)
    read_activity = models.ForeignKey(ReadActivity, on_delete=models.CASCADE, null=True, blank=True)
    rating_activity = models.ForeignKey(RatingActivity, on_delete=models.CASCADE, null=True, blank=True)

    def display_activity(self):
        datetime_display = self.datetime.strftime('%d.%m.%Y %H:%M')
        activity_string = None

        if self.follow_activity:
            activity_string = self.follow_activity.display_activity()
        elif self.new_thread_activity:
            activity_string = self.new_thread_activity.display_activity()
        elif self.new_post_activity:
            activity_string = self.new_post_activity.display_activity()
        elif self.want_to_read_activity:
            activity_string = self.want_to_read_activity.display_activity()
        elif self.currently_reading_activity:
            activity_string = self.currently_reading_activity.display_activity()
        elif self.read_activity:
            activity_string = self.read_activity.display_activity()
        elif self.rating_activity:
            activity_string = self.rating_activity.display_activity()

        final_string = mark_safe(f'{datetime_display}<br>{activity_string}')
        return final_string
