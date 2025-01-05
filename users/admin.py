from django.contrib import admin
from users.models import User


class UserAdmin(admin.ModelAdmin):
    model = User
    ordering = ('first_name', 'last_name', 'username')
    fields = ('first_name', 'last_name', 'username', 'email', 'password', 'is_superuser',
              'profile_picture', 'joined_date', 'level', 'xp', 'preferred_genres')
    list_display = ('first_name', 'last_name', 'username', 'email', 'password',
                    'is_superuser', 'profile_picture', 'joined_date', 'level',
                    'xp', 'preferred_genres_list')

    @staticmethod
    def preferred_genres_list(user):
        return ', '.join([genre.name for genre in user.preferred_genres.all()])


admin.site.register(User, UserAdmin)