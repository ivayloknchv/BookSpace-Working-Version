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
        return reverse("genre_detail", kwargs={"slug": self.slug})

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
        return reverse("author_detail", kwargs={"slug": self.slug})

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
        return reverse("book_detail", kwargs={"slug": self.slug})

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
        return reviews.aggregate(Avg('review_score'))['review_score__avg']

    @property
    def reviews_by_stars_count(self):
        reviews = self.bookreview_set.all()
        stars_count = {}
        for i in range(1, 6):
            stars_count[i] = reviews.filter(review_score=i).count()
        return stars_count


class BookReview(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_score = models.PositiveIntegerField(default=0)
    review_date = models.DateField()

    def __str__(self):
        return f'Review for {self.book.title} - {self.review_score}'


class ReadBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read_date = models.DateField()

    def __str__(self):
        return f'{self.book.title} read by {self.user} on {self.read_date}'