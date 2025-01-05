from django.contrib import admin
from books_database.models import (Genre, Author, Book, WantToReadBook,
                                   CurrentlyReadingBook, ReadBook, BookReview)

class GenreAdmin(admin.ModelAdmin):
    model = Genre
    search_fields = ('name',)
    ordering = ('name',)
    fields = ('name', 'slug')
    list_display = ('name', 'slug')


class AuthorAdmin(admin.ModelAdmin):
    model = Author
    search_fields = ('name',)
    ordering = ('name',)
    fields = ('name', 'slug')
    list_display = ('name', 'slug')


class BookAdmin(admin.ModelAdmin):
    model = Book
    ordering = ('title', 'author')
    search_fields = ('title',)
    fields = ('title', 'author', 'genres', 'cover_url', 'slug')
    list_display = ('title', 'author', 'genres_list', 'cover_url', 'slug')

    @staticmethod
    def genres_list(book):
        return ', '.join([genre.name for genre in book.genres.all()])


class WantToReadBookAdmin(admin.ModelAdmin):
    model = WantToReadBook
    ordering = ('add_date', )
    fields = ('book', 'user', 'add_date')
    list_display = ('book', 'user', 'add_date')


class CurrentlyReadingBookAdmin(admin.ModelAdmin):
    model = CurrentlyReadingBook
    ordering = ('add_date', )
    fields = ('book', 'user', 'add_date')
    list_display = ('book', 'user', 'add_date')


class ReadBookAdmin(admin.ModelAdmin):
    model = ReadBook
    ordering = ('book', 'user', 'read_date')
    fields = ('book', 'user', 'read_date')
    list_display = ('book', 'user', 'read_date')


class BookReviewAdmin(admin.ModelAdmin):
    model = BookReview
    ordering = ('review_date',)
    fields = ('book', 'review_user', 'review_score', 'review_date')
    list_display = ('book', 'review_user', 'review_score', 'review_date')


admin.site.register(Genre, GenreAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(WantToReadBook, WantToReadBookAdmin)
admin.site.register(CurrentlyReadingBook, CurrentlyReadingBookAdmin)
admin.site.register(ReadBook, ReadBookAdmin)
admin.site.register(BookReview, BookReviewAdmin)