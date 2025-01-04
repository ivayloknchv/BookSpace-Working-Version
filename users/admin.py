from django.contrib import admin
from users.models import User


class UserAdmin(admin.ModelAdmin):
    model = User
    ordering = ('first_name', 'last_name', 'username')
    fields = ('first_name', 'last_name', 'username', 'email', 'password', 'is_superuser', 'profile_picture',
              'joined_date', 'level', 'xp', 'preferred_genres', 'want_to_read_books',
              'currently_reading_books')
    list_display = ('first_name', 'last_name', 'username', 'email', 'password', 'is_superuser',
                    'profile_picture', 'joined_date', 'level', 'xp', 'preferred_genres_list',
                    'want_to_read_books_list','currently_reading_books_list')

    def preferred_genres_list(self, user):
        return ', '.join([genre.name for genre in user.preferred_genres.all()])

    def want_to_read_books_list(self, user):
        return ', '.join([book.title for book in user.want_to_read_books.all()])

    def currently_reading_books_list(self, user):
        return ', '.join([book.title for book in user.currently_reading_books.all()])


admin.site.register(User, UserAdmin)