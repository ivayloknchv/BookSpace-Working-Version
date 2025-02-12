from django.contrib import admin
from users.models import User, FollowRelation


class UserAdmin(admin.ModelAdmin):
    model = User
    ordering = ('first_name', 'last_name', 'username')
    fields = ('first_name', 'last_name', 'username', 'email', 'password', 'is_superuser',
              'profile_picture', 'joined_date', 'preferred_genres')
    list_display = ('first_name', 'last_name', 'username', 'email', 'password',
                    'is_superuser', 'profile_picture', 'joined_date', 'preferred_genres_list')

    @staticmethod
    def preferred_genres_list(user):
        return ', '.join([genre.name for genre in user.preferred_genres.all()])



class FollowRelationAdmin(admin.ModelAdmin):
    model = FollowRelation
    ordering = ('date_time',)
    fields = ('follower', 'followed', 'date_time')
    list_display = ('follower', 'followed', 'date_time')


admin.site.register(User, UserAdmin)
admin.site.register(FollowRelation, FollowRelationAdmin)