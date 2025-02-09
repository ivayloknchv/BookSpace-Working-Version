from django.contrib import admin
from forum.models import Category, Thread, Post


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    ordering = ('name', 'description', 'slug')
    fields = ('name', 'description', 'slug')
    list_display = ('name', 'description', 'slug')


class ThreadAdmin(admin.ModelAdmin):
    model = Thread
    ordering = ('title', 'category', 'author', 'created_datetime', 'slug')
    fields = ('title', 'category', 'author', 'created_datetime', 'slug')
    list_display = ('title', 'category', 'author', 'created_datetime', 'slug')


class PostAdmin(admin.ModelAdmin):
    model = Post
    ordering = ('author', 'thread', 'post_datetime', 'caption')
    fields = ('author', 'thread', 'post_datetime', 'caption')
    list_display = ('author', 'thread', 'post_datetime', 'caption')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Post, PostAdmin)