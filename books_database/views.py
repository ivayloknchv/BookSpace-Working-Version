from django.db.models import Count
from django.contrib import messages
from datetime import date, datetime
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from books_database.models import Book, Genre, Author, ReadBook, BookReview


RECOMMENDATIONS_TO_SHOW = 12


def create_recommendations(book):
   recommendations = (Book.objects.filter(author=book.author) |
                     Book.objects.filter(genres__in=book.genres.all()))

   recommendations = recommendations.exclude(id=book.id)

   if recommendations.count() < RECOMMENDATIONS_TO_SHOW:
      recommendations = recommendations.order_by('?')[:recommendations.count()]
   else:
      recommendations = recommendations.order_by('?')[:RECOMMENDATIONS_TO_SHOW]

   return recommendations

def view_book(request, slug):
   user = request.user
   book = Book.objects.get(slug=slug)
   stars_count = book.reviews_by_stars_count
   recommendations = create_recommendations(book)

   if user.is_authenticated:
      is_in_wanted = user.want_to_read_books.filter(id=book.id).exists()
      is_currently_reading = user.currently_reading_books.filter(id=book.id).exists()
      is_read = ReadBook.objects.filter(book_id=book.id, user_id=user.id).exists()
      has_status = is_in_wanted or is_currently_reading or is_read
      is_reviewed = BookReview.objects.filter(book_id=book.id, review_user_id=user.id).exists()

      user_score = None
      if is_reviewed:
         user_score = BookReview.objects.get(book_id=book.id, review_user_id=user.id)

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
   genres_paginator = Paginator(all_genres, 20)
   current_page = genres_paginator.get_page(page_num)
   return  render(request, 'all_genres.html',
                  {'current_page' : current_page, 'sort' : sort})

def preview_genre(request, slug):
   genre = Genre.objects.get(slug=slug)
   books = Book.objects.filter(genres=genre).order_by('title')
   books_paginator = Paginator(books, 20)
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
   authors_paginator= Paginator(all_authors, 20)
   current_page = authors_paginator.get_page(page_num)
   return render(request, 'all_authors.html',
   {'current_page' : current_page, 'sort' : sort})

def preview_author(request, slug):
   author = Author.objects.get(slug=slug)
   books = Book.objects.filter(author=author).order_by('title')
   books_paginator = Paginator(books, 20)
   page_num = request.GET.get('page', 1)
   current_page = books_paginator.get_page(page_num)
   return render(request, 'preview_author.html',
                 {'author' : author, 'current_page' : current_page})

@login_required(login_url='/login/')
def handle_book_status(request, slug):

   user = request.user
   book = Book.objects.get(slug=slug)

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
   if user.currently_reading_books.filter(id=book.id).exists():
      user.currently_reading_books.remove(book)
   if ReadBook.objects.filter(book_id=book.id, user_id=user.id).exists():
      ReadBook.objects.filter(book_id=book.id, user_id=user.id).delete()
   user.want_to_read_books.add(book)

def handle_currently_reading(user, book):
   if user.want_to_read_books.filter(id=book.id).exists():
      user.want_to_read_books.remove(book)
   if ReadBook.objects.filter(book_id=book.id, user_id=user.id).exists():
      ReadBook.objects.filter(book_id=book.id, user_id=user.id).delete()
   user.currently_reading_books.add(book)

def handle_read(user, book):
   if user.want_to_read_books.filter(id=book.id).exists():
      user.want_to_read_books.remove(book)
   if user.currently_reading_books.filter(id=book.id).exists():
      user.currently_reading_books.remove(book)
   read_book, is_created = ReadBook.objects.get_or_create(book_id = book.id, user_id = user.id,
                                              defaults={'read_date' : datetime.today()})
   read_book.save()

def handle_reset(user, book):
   if user.want_to_read_books.filter(id=book.id).exists():
      user.want_to_read_books.remove(book)
   if user.currently_reading_books.filter(id=book.id).exists():
      user.currently_reading_books.remove(book)
   if ReadBook.objects.filter(book_id=book.id, user_id=user.id).exists():
      ReadBook.objects.filter(book_id=book.id, user_id=user.id).delete()

def handle_book_review(request, slug):
   user = request.user
   book = Book.objects.get(slug=slug)

   if request.method == 'POST':
      stars = request.POST.get('stars', None)

      if stars is None:
         messages.error(request, 'Please choose your rating!')
         return redirect('book', slug)

      review, review_created= BookReview.objects.get_or_create(book_id=book.id,
         review_user_id=user.id,
         defaults={'review_score': stars, 'review_date': date.today(),})

      if not review_created:
         review.review_score = stars
         review.review_date = date.today()
         review.save()

      handle_read(user, book)
      messages.success(request, f'You rated {book.title} with {stars} stars!')

   return redirect('book', slug)

def remove_review(request, slug):
   user = request.user
   book = Book.objects.get(slug=slug)

   if BookReview.objects.filter(book_id=book.id, review_user_id=user.id).exists():
      BookReview.objects.filter(book_id=book.id, review_user_id=user.id).delete()
   messages.success(request, f'You removed your review for {book.title}!')
   return redirect('book', slug)
