from datetime import timedelta
from django.shortcuts import render
from django.utils.timezone import now
from users.models import FollowRelation
from activities.models import ActivityWrapper
from books_database.models import Book, CurrentlyReadingBook, ReadBook, BookReview


RECENT_ACTIVITIES = 20
BOOKS_TO_DISPLAY_AUTHENTICATED = 40
BOOKS_TO_DISPLAY_UNAUTHENTICATED = 80


def get_displayed_books(user):
    """For authenticated users with set preferred genres chose
       randomly 20 books from their favourite genres list
       Otherwise just display 20 completely random books"""

    if user.is_authenticated and user.preferred_genres.count():
        return Book.objects.filter(genres__in=user.preferred_genres.all()).order_by('?')[:BOOKS_TO_DISPLAY_AUTHENTICATED]
    return Book.objects.all().order_by('?')[:BOOKS_TO_DISPLAY_UNAUTHENTICATED]

def get_unfinished_books(user):
    """"Return all book that a certain user
     has been reading for more than five days"""

    five_days_ago = now() - timedelta(days=5)
    all_currently_reading_books = CurrentlyReadingBook.objects.filter(user=user, date__lt=five_days_ago).values_list('book_id', flat=True)
    unfinished_books = Book.objects.filter(id__in=all_currently_reading_books).order_by('title')
    return unfinished_books

def get_unreviewed_books(user):
    """Return all read but unreviewed
    books by a certain user"""

    all_reviews = BookReview.objects.filter(user=user).values_list('book_id', flat=True)
    all_read_books = ReadBook.objects.filter(user=user).values_list('book_id', flat=True)
    unreviewed_books = Book.objects.filter(id__in=all_read_books).exclude(id__in=all_reviews).order_by('title')
    return unreviewed_books

def home(request):
    user=request.user
    displayed_books = get_displayed_books(user)

    if request.user.is_authenticated:
        followed = FollowRelation.objects.filter(follower=request.user).values_list('followed')
        activities = ActivityWrapper.objects.filter(initiator__in=followed).order_by('-datetime')[:RECENT_ACTIVITIES]
        unfinished_books = get_unfinished_books(user)
        unreviewed_books = get_unreviewed_books(user)
        return render(request,'homepage_authenticated.html',{
            'logged_user' : request.user, 'displayed_books' : displayed_books, 'activities' : activities,
            'unfinished_books' : unfinished_books, 'unreviewed_books' : unreviewed_books })

    return render(request,'homepage.html', {'displayed_books' : displayed_books})






