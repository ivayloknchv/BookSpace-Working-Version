from django.shortcuts import render
from books_database.models import Book
from activities.models import ActivityWrapper
from users.models import FollowRelation

BOOKS_TO_DISPLAY = 20
RECENT_ACTIVITIES = 20

def handle_displayed_books(user):
    """For authenticated users with set preferred genres chose
       randomly 20 books from their favourite genres list
       Otherwise just display 20 completely random books"""

    if user.is_authenticated and user.preferred_genres.count():
        return Book.objects.filter(genres__in=user.preferred_genres.all()).order_by('?')[:BOOKS_TO_DISPLAY]
    return Book.objects.all().order_by('?')[:BOOKS_TO_DISPLAY]

def home(request):
    displayed_books = handle_displayed_books(request.user)
    if request.user.is_authenticated:
        followed = FollowRelation.objects.filter(follower=request.user).values_list('followed')
        activities = ActivityWrapper.objects.filter(initiator__in=followed).order_by('-datetime')[:RECENT_ACTIVITIES]
        return render(request,'homepage_authenticated.html',
{'logged_user' : request.user, 'displayed_books' : displayed_books, 'activities' : activities})
    return render(request,'homepage.html', {'displayed_books' : displayed_books})






