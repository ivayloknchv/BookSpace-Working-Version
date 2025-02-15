from django.db import models
from django.db.models import Avg
from django.utils.text import slugify
from users.models import User
from django.urls import reverse


class Genre(models.Model):
    name = models.CharField(max_length=63, unique=True)
    slug = models.SlugField(null=True, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('preview_genre', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('preview_author', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)
        self.slug = f'{slugify(self.name, allow_unicode=True)}-{self.pk}'
        super().save(*args, **kwargs)


class Book(models.Model):
    title = models.CharField(max_length=255, unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre)
    description = models.CharField(max_length=1000, default='No description')
    cover_url = models.URLField()
    slug = models.SlugField(unique=True, null=True)

    def __str__(self):
        return f'{self.title} by {self.author}'

    def get_absolute_url(self):
        return reverse('book', kwargs={'slug' : self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            new_slug = slugify(self.title, allow_unicode=True)
            self.slug = new_slug
        super().save(*args, **kwargs)
        self.slug = f'{slugify(self.title, allow_unicode=True)}-{self.pk}'
        super().save(*args, **kwargs)

    @property
    def avg_review(self):
        reviews = self.bookreview_set.all()
        return reviews.aggregate(Avg('score'))['score__avg']

    @property
    def reviews_by_stars_count(self):
        reviews = self.bookreview_set.all()
        stars_count = {}
        for i in range(1, 6):
            stars_count[i] = reviews.filter(score=i).count()
        return stars_count


class BookStatus(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class WantToReadBook(BookStatus):

    class Meta:
        verbose_name_plural = 'Want To Read Books'

        def __str__(self):
            return f'{self.user} wants to read {self.book}'


class CurrentlyReadingBook(BookStatus):

    class Meta:
        verbose_name_plural = 'Currently Reading Books'

    def __str__(self):
        return f'{self.user} is currently reading {self.book}'


class ReadBook(BookStatus):

    class Meta:
        verbose_name_plural = 'Read Books'

    def __str__(self):
        return f'{self.book.title} read by {self.user} on {self.read_date}'


class BookReview(BookStatus):
    score = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Book Reviews'

    def __str__(self):
        return f'Review for {self.book.title} - {self.score}'


