from django.contrib import admin
from books_database.models import Genre, Book, BookReview, ReadBook, Author

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
    list_display = ('display_name', 'slug')

    def display_name(self, author):
        return author.name


class BookAdmin(admin.ModelAdmin):
    model = Book
    ordering = ('title', 'author')
    search_fields = ('title',)
    fields = ('title', 'author', 'genres', 'cover_url', 'slug')
    list_display = ('title', 'author', 'genres_list', 'cover_url', 'slug')

    def genres_list(self, book):
        return ', '.join([genre.name for genre in book.genres.all()])


class BookReviewAdmin(admin.ModelAdmin):
    model = BookReview
    ordering = ('review_date',)
    fields =('book', 'review_user', 'review_score', 'review_date')
    list_display = ('book', 'review_user', 'review_score', 'review_date')


class ReadBookAdmin(admin.ModelAdmin):
    model = ReadBook
    ordering = ('book', 'user', 'read_date')
    fields = ('book', 'user', 'read_date')
    list_display = ('book', 'user', 'read_date')


admin.site.register(Genre, GenreAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookReview, BookReviewAdmin)
admin.site.register(ReadBook, ReadBookAdmin)