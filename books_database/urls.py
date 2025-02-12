from django.urls import path
from . import views

urlpatterns = [
    path('book/<str:slug>/', views.view_book, name='book'),
    path('genres/', views.view_all_genres, name='genres'),
    path('genres/<str:slug>/', views.preview_genre, name='preview_genre'),
    path('authors/', views.view_all_authors, name='authors'),
    path('authors/<str:slug>/', views.preview_author, name='preview_author'),
    path('book/<str:slug>/status/', views.handle_book_status, name='handle_book_status'),
    path('book/<str:slug>/review/', views.handle_book_review, name='handle_book_review'),
    path('book/<str:slug>/clear_review/', views.remove_review, name='remove_review'),
]
