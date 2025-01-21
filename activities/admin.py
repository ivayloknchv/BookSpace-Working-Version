from django.contrib import admin
from .models import (FollowActivity, WantToReadActivity,
                    CurrentlyReadingActivity, ReadActivity, RatingActivity)


class FollowActivityAdmin(admin.ModelAdmin):
    model = FollowActivity
    ordering = ('initiator', 'activity_datetime', 'followed_user')
    fields = ('initiator', 'activity_datetime', 'followed_user')
    list_display = ('initiator', 'activity_datetime', 'followed_user')


class WantToReadActivityAdmin(admin.ModelAdmin):
    model = WantToReadActivity
    ordering = ('initiator', 'activity_datetime', 'book')
    fields = ('initiator', 'activity_datetime', 'book')
    list_display = ('initiator', 'activity_datetime', 'book')


class CurrentlyReadingActivityAdmin(admin.ModelAdmin):
    model = CurrentlyReadingActivity
    ordering = ('initiator', 'activity_datetime', 'book')
    fields = ('initiator', 'activity_datetime', 'book')
    list_display = ('initiator', 'activity_datetime', 'book')


class ReadActivityAdmin(admin.ModelAdmin):
    model = ReadActivity
    ordering = ('initiator', 'activity_datetime', 'book')
    fields = ('initiator', 'activity_datetime', 'book')
    list_display = ('initiator', 'activity_datetime', 'book')


class RatingActivityAdmin(admin.ModelAdmin):
    model = RatingActivity
    ordering = ('initiator', 'activity_datetime', 'book', 'stars')
    fields = ('initiator', 'activity_datetime', 'book', 'stars')
    list_display = ('initiator', 'activity_datetime', 'book', 'stars')


admin.site.register(FollowActivity, FollowActivityAdmin)
admin.site.register(WantToReadActivity, WantToReadActivityAdmin)
admin.site.register(CurrentlyReadingActivity, CurrentlyReadingActivityAdmin)
admin.site.register(ReadActivity, ReadActivityAdmin)
admin.site.register(RatingActivity, RatingActivityAdmin)
