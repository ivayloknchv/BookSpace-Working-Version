from django.shortcuts import render
from books_database.models import Book
from django.core.paginator import Paginator


def search(request):
    if request.method == 'GET':
        query = request.GET.get('q', '').strip()
        context = {}
        if query:
            found_books_by_title = Book.objects.filter(title__icontains=query)
            found_books_by_author = Book.objects.filter(author__name__icontains=query)
            found_books = ( found_books_by_title |  found_books_by_author).distinct()
            found_books_paginator = Paginator(found_books, 20)
            page_num = request.GET.get('page', 1)
            current_page =  found_books_paginator.get_page(page_num)
            context = {'current_page' : current_page, 'q' : query, 'total_results' : found_books.count()}

        return render(request, 'search.html', context)