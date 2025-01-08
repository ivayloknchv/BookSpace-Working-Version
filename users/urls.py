from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_, name='signup'),
    path('signup_preferred_genres/', views.signup_pick_preferred_genres, name='signup_preferred_genres'),
    path('login/', views.login_, name='login'),
    path('profile/<str:username>/', views.view_profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('edit_profile/user_data_change/', views.user_data_change, name='user_data_change'),
    path('edit_profile/password_change/', views.password_change, name='password_change'),
    path('edit_profile/genres_change/', views.genres_change, name='genres_change'),
    path('edit_profile/delete_account/', views.delete_account, name='delete_account'),
    path('logout/', views.logout_, name='logout'),
    path('profile/<str:username>/read_books', views.read_books, name='read_books'),
    path('profile/<str:username>/currently_reading_books', views.currently_reading_books,
         name='currently_reading_books'),
    path('profile/<str:username>/want_to_read_books', views.want_to_read_books,
         name='want_to_read_books'),
    path('follow/<str:username>', views.follow_user, name='follow_user'),
    path('unfollow/<str:username>', views.unfollow_user, name='unfollow_user'),
    path('profile/<str:username>/followers', views.view_followers, name='followers'),
    path('profile/<str:username>/following', views.view_following, name='following'),
]
