from django.http import Http404
from users.models import User
from django.shortcuts import render
from books_database.models import Book
from django.core.paginator import Paginator

RESULTS_PER_PAGE = 20


def get_searched_books(query):
    found_books_by_title = Book.objects.filter(title__icontains=query)
    found_books_by_author = Book.objects.filter(author__name__icontains=query)
    found_books = (found_books_by_title | found_books_by_author).distinct()
    return found_books

def get_searched_users(query):
    found_users_by_first_name = User.objects.filter(first_name__icontains=query)
    found_users_by_last_name = User.objects.filter(last_name__icontains=query)
    found_users_by_username = User.objects.filter(username__icontains=query)
    found_users = (found_users_by_username | found_users_by_first_name | found_users_by_last_name).distinct()
    return found_users


def search(request):
    if request.method == 'GET':
        query = request.GET.get('q', '').strip()
        results = request.GET.get('results', 'books')

        context = {}

        if query:
            found_results = None

            if results == 'books':
                found_results = get_searched_books(query)
            elif results == 'users':
                found_results = get_searched_users(query)
            found_results_paginator = Paginator(found_results, RESULTS_PER_PAGE)
            page_num = request.GET.get('page', 1)
            current_page =  found_results_paginator.get_page(page_num)
            context = {'current_page' : current_page, 'q' : query, 'results' : results,
                       'total_results' : found_results.count()}

        return render(request, 'search.html', context)
