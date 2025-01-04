from django.shortcuts import render
from books_database.models import Book


BOOKS_TO_DISPLAY = 20

def handle_displayed_books(user):
    """For authenticated users with set preferred genres chose
       randomly 20 books from their favourite genres list
       Otherwise just display 20 completely random books"""

    if user.is_authenticated and user.preferred_genres.count():
        return Book.objects.filter(genres__in=user.preferred_genres.all()).order_by('?')[:BOOKS_TO_DISPLAY]
    return Book.objects.all().order_by('?')[:20]

def home(request):
    displayed_books = handle_displayed_books(request.user)
    if request.user.is_authenticated:
        return render(request,'homepage_authenticated.html',
{'logged_user' : request.user, 'displayed_books' : displayed_books})
    return render(request,'homepage.html', {'displayed_books' : displayed_books})






