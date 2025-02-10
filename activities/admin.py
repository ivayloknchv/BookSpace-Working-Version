from django.contrib import admin
from .models import (FollowActivity, NewThreadActivity, WantToReadActivity,
                    CurrentlyReadingActivity, ReadActivity, RatingActivity, ActivityWrapper)


class FollowActivityAdmin(admin.ModelAdmin):
    model = FollowActivity
    ordering = ('initiator', 'followed_user')
    fields = ('initiator', 'followed_user')
    list_display = ('initiator', 'followed_user')


class NewThreadActivityAdmin(admin.ModelAdmin):
    model = NewThreadActivity
    ordering = ('initiator', 'thread')
    fields = ('initiator', 'thread')
    list_display = ('initiator', 'thread')


class WantToReadActivityAdmin(admin.ModelAdmin):
    model = WantToReadActivity
    ordering = ('initiator', 'book')
    fields = ('initiator', 'book')
    list_display = ('initiator', 'book')


class CurrentlyReadingActivityAdmin(admin.ModelAdmin):
    model = CurrentlyReadingActivity
    ordering = ('initiator', 'book')
    fields = ('initiator', 'book')
    list_display = ('initiator', 'book')


class ReadActivityAdmin(admin.ModelAdmin):
    model = ReadActivity
    ordering = ('initiator', 'book')
    fields = ('initiator', 'book')
    list_display = ('initiator', 'book')


class RatingActivityAdmin(admin.ModelAdmin):
    model = RatingActivity
    ordering = ('initiator', 'book', 'stars')
    fields = ('initiator', 'book', 'stars')
    list_display = ('initiator', 'book', 'stars')


class ActivityWrapperAdmin(admin.ModelAdmin):
    model = ActivityWrapper
    ordering = ('initiator', 'datetime', 'follow_activity', 'new_thread_activity', 'want_to_read_activity',
                'currently_reading_activity', 'read_activity', 'rating_activity')
    fields = ('initiator', 'datetime', 'follow_activity', 'new_thread_activity', 'want_to_read_activity',
              'currently_reading_activity', 'read_activity', 'rating_activity')
    list_display = ('initiator', 'datetime', 'follow_activity', 'new_thread_activity', 'want_to_read_activity',
                    'currently_reading_activity', 'read_activity', 'rating_activity')


admin.site.register(FollowActivity, FollowActivityAdmin)
admin.site.register(NewThreadActivity, NewThreadActivityAdmin)
admin.site.register(WantToReadActivity, WantToReadActivityAdmin)
admin.site.register(CurrentlyReadingActivity, CurrentlyReadingActivityAdmin)
admin.site.register(ReadActivity, ReadActivityAdmin)
admin.site.register(RatingActivity, RatingActivityAdmin)
admin.site.register(ActivityWrapper, ActivityWrapperAdmin)
