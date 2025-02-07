from django.contrib import admin
from .models import (FollowActivity, WantToReadActivity,
                    CurrentlyReadingActivity, ReadActivity, RatingActivity, ActivityWrapper)


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


class ActivityWrapperAdmin(admin.ModelAdmin):
    model = ActivityWrapper
    ordering = ('initiator', 'datetime', 'follow_activity', 'want_to_read_activity', 'currently_reading_activity',
                'read_activity', 'rating_activity')
    fields = ('initiator', 'datetime', 'follow_activity', 'want_to_read_activity', 'currently_reading_activity',
                'read_activity', 'rating_activity')
    list_display = ('initiator', 'datetime', 'follow_activity', 'want_to_read_activity', 'currently_reading_activity',
                'read_activity', 'rating_activity')


admin.site.register(FollowActivity, FollowActivityAdmin)
admin.site.register(WantToReadActivity, WantToReadActivityAdmin)
admin.site.register(CurrentlyReadingActivity, CurrentlyReadingActivityAdmin)
admin.site.register(ReadActivity, ReadActivityAdmin)
admin.site.register(RatingActivity, RatingActivityAdmin)
admin.site.register(ActivityWrapper, ActivityWrapperAdmin)
