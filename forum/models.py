from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Thread(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Threads'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
            super().save(*args, **kwargs)
        updated_slug = f'{self.slug}-{self.pk}'
        self.slug = updated_slug
        super().save(*args, **kwargs)


class Post(models.Model):
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    post_datetime = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(max_length=2048)

    class Meta:
        verbose_name_plural = 'Posts'

    def __str__(self):
        return f'{self.pk}'

    @property
    def likes_count(self):
        return LikeRelation.objects.filter(post=self).count()

    @property
    def liked_by(self):
        return LikeRelation.objects.filter(post=self).order_by('-like_datetime')


class LikeRelation(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Like Relations'

    def __str__(self):
        return f'{self.user} liked {self.post.author}\'s post in {self.post.thread}'