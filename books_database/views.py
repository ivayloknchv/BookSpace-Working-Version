from django.db.models import Count
from django.contrib import messages

from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from books_database.models import (Book, Genre, Author, WantToReadBook,
                                   CurrentlyReadingBook, ReadBook, BookReview)
from activities.models import (WantToReadActivity, CurrentlyReadingActivity, ReadActivity,
                               RatingActivity, ActivityWrapper)


BOOKS_PER_PAGE = 20
RECOMMENDATIONS_TO_SHOW = 12


def create_recommendations(book):
   recommendations = (Book.objects.filter(author=book.author) |
                     Book.objects.filter(genres__in=book.genres.all()))

   recommendations = recommendations.exclude(id=book.id)
   recommendations = recommendations.order_by('?')[:RECOMMENDATIONS_TO_SHOW]
   return recommendations

def view_book(request, slug):
   user = request.user
   book = get_object_or_404(Book,slug=slug)
   stars_count = book.reviews_by_stars_count
   recommendations = create_recommendations(book)

   if user.is_authenticated:
      is_in_wanted = WantToReadBook.objects.filter(book=book, user=user).exists()
      is_currently_reading = CurrentlyReadingBook.objects.filter(book=book, user=user).exists()
      is_read = ReadBook.objects.filter(book=book, user=user).exists()
      has_status = is_in_wanted or is_currently_reading or is_read
      is_reviewed = BookReview.objects.filter(book=book, user=user).exists()

      user_score = None
      if is_reviewed:
         user_score = BookReview.objects.get(book=book, user=user)

      return render(request, 'book.html',
                    {'book' : book, 'is_in_wanted' : is_in_wanted,
      'is_currently_reading' : is_currently_reading, 'is_read' : is_read,
      'has_status' : has_status, 'is_reviewed' : is_reviewed, 'user_score' : user_score,
      'stars_count' : stars_count, 'recommendations' : recommendations})

   return render(request, 'book.html',
                 {'book': book, 'is_in_wanted': False,
                  'is_currently_reading': False, 'is_read': False,
                  'has_status': False, 'is_reviewed': False, 'user_score': None,
                  'stars_count': stars_count, 'recommendations': recommendations})

def sort_genres(sort):
   if sort == 'namesAsc':
      return Genre.objects.annotate(book_count=Count('book')).order_by('name')
   elif sort == 'namesDesc':
      return Genre.objects.annotate(book_count=Count('book')).order_by('-name')
   elif sort == 'countAsc':
      return Genre.objects.annotate(book_count=Count('book')).order_by('book_count')
   elif sort == 'countDesc':
      return Genre.objects.annotate(book_count=Count('book')).order_by('-book_count')

def view_all_genres(request):
   page_num = request.GET.get('page', 1)
   sort = request.GET.get('sort', 'countDesc')
   all_genres = sort_genres(sort)
   genres_paginator = Paginator(all_genres, BOOKS_PER_PAGE)
   current_page = genres_paginator.get_page(page_num)
   return  render(request, 'all_genres.html',
                  {'current_page' : current_page, 'sort' : sort})

def preview_genre(request, slug):
   genre = get_object_or_404(Genre, slug=slug)
   books = Book.objects.filter(genres=genre).order_by('title')
   books_paginator = Paginator(books, BOOKS_PER_PAGE)
   page_num = request.GET.get('page', 1)
   current_page = books_paginator.get_page(page_num)
   return render(request, 'preview_genre.html',
                 {'genre': genre, 'current_page' : current_page})

def sort_authors(sort):
   if sort == 'namesAsc':
      return Author.objects.annotate(book_count=Count('book')).order_by('name')
   elif sort == 'namesDesc':
      return Author.objects.annotate(book_count=Count('book')).order_by('-name')
   elif sort == 'countAsc':
      return Author.objects.annotate(book_count=Count('book')).order_by('book_count')
   elif sort == 'countDesc':
      return Author.objects.annotate(book_count=Count('book')).order_by('-book_count')

def view_all_authors(request):
   page_num = request.GET.get('page', 1)
   sort = request.GET.get('sort', 'countDesc')
   all_authors = sort_authors(sort)
   authors_paginator= Paginator(all_authors, BOOKS_PER_PAGE)
   current_page = authors_paginator.get_page(page_num)
   return render(request, 'all_authors.html',
   {'current_page' : current_page, 'sort' : sort})

def preview_author(request, slug):
   author = get_object_or_404(Author, slug=slug)
   books = Book.objects.filter(author=author).order_by('title')
   books_paginator = Paginator(books, BOOKS_PER_PAGE)
   page_num = request.GET.get('page', 1)
   current_page = books_paginator.get_page(page_num)
   return render(request, 'preview_author.html',
                 {'author' : author, 'current_page' : current_page})

@login_required(login_url='/login/')
def handle_book_status(request, slug):

   user = request.user
   book = get_object_or_404(Book, slug=slug)

   if request.method == 'POST':
      handle_type = request.POST.get('handle_type')

      if handle_type == 'want_to_read':
         messages.success(request, f'You added {book.title} to your wanted to read list!')
         handle_want_to_read(user, book)
      elif handle_type == 'currently_reading':
         messages.success(request, f'You added {book.title} to your currently reading list!')
         handle_currently_reading(user, book)
      elif handle_type == 'read':
         messages.success(request, f'You added {book.title} to your read list!')
         handle_read(user, book)
      elif handle_type == 'reset':
         messages.success(request, f'You reset the reading status of {book.title}!')
         handle_reset(user, book)

   return redirect('book', slug)

def handle_want_to_read(user, book):
   CurrentlyReadingBook.objects.filter(book=book, user=user).delete()
   ReadBook.objects.filter(book=book, user=user).delete()
   want_to_read_book, is_created = WantToReadBook.objects.get_or_create(book=book, user=user)

   if is_created:
      want_to_read_activity = WantToReadActivity(book=book, initiator=user)
      want_to_read_activity.save()
      want_to_read_activity_wrapper = ActivityWrapper(initiator=user,
                                                      want_to_read_activity = want_to_read_activity)
      want_to_read_activity_wrapper.save()

def handle_currently_reading(user, book):
   WantToReadBook.objects.filter(book=book, user=user).delete()
   ReadBook.objects.filter(book=book, user=user).delete()
   currently_reading, is_created = CurrentlyReadingBook.objects.get_or_create(book=book, user=user)

   if is_created:
      currently_reading_activity = CurrentlyReadingActivity(book=book, initiator=user)
      currently_reading_activity.save()
      currently_reading_activity_wrapper = ActivityWrapper(initiator=user,
                                                           currently_reading_activity=currently_reading_activity)
      currently_reading_activity_wrapper.save()

def handle_read(user, book):
   WantToReadBook.objects.filter(book=book, user=user).delete()
   CurrentlyReadingBook.objects.filter(book=book, user=user).delete()
   read_book, is_created = ReadBook.objects.get_or_create(book = book, user = user)

   if is_created:
      read_activity = ReadActivity(book=book, initiator=user)
      read_activity.save()
      read_activity_wrapper = ActivityWrapper(initiator=user, read_activity = read_activity)
      read_activity_wrapper.save()

def handle_reset(user, book):
   WantToReadBook.objects.filter(book=book, user=user).delete()
   CurrentlyReadingBook.objects.filter(book=book, user=user).delete()
   ReadBook.objects.filter(book=book, user=user).delete()

def handle_book_review(request, slug):
   user = request.user
   book = get_object_or_404(Book, slug=slug)

   if request.method == 'POST':
      stars = request.POST.get('stars', None)

      if stars is None:
         messages.error(request, 'Please choose your rating!')
         return redirect('book', slug)

      review, review_created= BookReview.objects.get_or_create(book=book, user=user, defaults={'score': stars})

      if not review_created:
         rating_activity = RatingActivity(initiator=user, book=book, stars=stars)
         rating_activity.save()
         rating_activity_wrapper = ActivityWrapper(initiator=user, rating_activity = rating_activity)
         rating_activity_wrapper.save()

      handle_read(user, book)
      messages.success(request, f'You rated {book.title} with {stars} stars!')

   return redirect('book', slug)

def remove_review(request, slug):
   user = request.user
   book = get_object_or_404(Book, slug=slug)
   BookReview.objects.filter(book=book, user=user).delete()
   messages.success(request, f'You removed your review for {book.title}!')
   return redirect('book', slug)