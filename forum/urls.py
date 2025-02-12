from django.urls import path
from . import views

urlpatterns = [
    path('forum/', views.show_forum_homepage, name='forum_homepage'),
    path('forum/categories/<str:slug>/', views.show_category, name='show_category'),
    path('forum/categories/<str:slug>/create_thread/', views.create_thread, name='create_thread'),
    path('forum/categories/<str:slug>/save_thread/', views.save_thread, name='save_thread'),
    path('forum/threads/<str:slug>/', views.view_thread, name='view_thread'),
    path('forum/threads/<str:slug>/add_reply/', views.add_reply, name='add_reply'),
    path('forum/like/<int:pk>/', views.like_post, name='like_post'),
    path('forum/unlike/<int:pk>/', views.unlike_post, name='unlike_post'),
]
