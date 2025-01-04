"""
URL configuration for course_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
