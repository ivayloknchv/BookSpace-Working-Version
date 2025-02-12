from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from users.models import User, FollowRelation
from books_database.models import Genre, CurrentlyReadingBook, WantToReadBook, ReadBook, BookReview
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from .forms import (MyLoginForm, MyUpdatePictureForm, MySignupForm, MySignupGenresForm, MyEditProfileForm,
                    MyPasswordChangeForm, MyChangeGenresForm)
from activities.models import FollowActivity, ActivityWrapper


BOOKS_PER_PAGE = 10
ACCOUNTS_PER_PAGE = 20
RECENT_ACTIVITIES = 20


def signup_(request):
    if request.method == 'POST':
        signup_form = MySignupForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            user.save()
            picture_form = MyUpdatePictureForm(data=request.POST, files=request.FILES, instance=user)
            picture_form.save()
            login(request, user)
            return redirect('signup_preferred_genres')
    else:
        signup_form = MySignupForm()
        picture_form = MyUpdatePictureForm()
    return render(request, 'signup.html', {'signup_form' : signup_form, 'picture_form' : picture_form})

@login_required(login_url='/login/')
def signup_pick_preferred_genres(request):
    if request.method == 'POST':
        form = MySignupGenresForm(request.POST)
        if form.is_valid():
            user = request.user
            preferred_genres = form.cleaned_data['preferred_genres']
            genres = Genre.objects.filter(name__in=preferred_genres)
            user.preferred_genres.set(genres)
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = MySignupGenresForm()
    return render(request, 'signup_preferred_genres.html', {'form' : form})

def login_(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = MyLoginForm(request, data=request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            to_redirect = request.GET.get('next', 'home')
            return redirect(to_redirect)
        else:
            messages.error(request,'Invalid credentials!')
    else:
        form = MyLoginForm(request, data=request.POST)
    return render(request, 'login.html', {'form' : form})

@login_required(login_url='/login/')
def logout_(request):
    logout(request)
    return redirect('home')

@login_required(login_url='/login/')
def view_profile(request, username):
    user = User.objects.get(username=username)
    is_followed = FollowRelation.objects.filter(follower=request.user,followed=user).exists()
    following_count = FollowRelation.objects.filter(follower=user).count()
    followers_count = FollowRelation.objects.filter(followed=user).count()

    activities = ActivityWrapper.objects.filter(initiator=user).order_by('-datetime')[:RECENT_ACTIVITIES]

    return render(request, 'user.html', {'user' : user, 'is_followed' : is_followed,
                   'following_count' : following_count, 'followers_count' :  followers_count,
                                                    'activities' : activities})

@login_required(login_url='/login/')
def edit_profile(request):
    user_data_form = MyEditProfileForm(instance=request.user)
    picture_form = MyUpdatePictureForm(instance=request.user)
    password_form = MyPasswordChangeForm(request.user)
    genres_form = MyChangeGenresForm(instance=request.user)
    return render(request, 'edit_profile.html',{'user_data_form' :  user_data_form,
        'picture_form' : picture_form, 'password_form' : password_form, 'genres_form' : genres_form})

@login_required(login_url='/login/')
def user_data_change(request):
    if request.method == 'POST':
        data_form = MyEditProfileForm(data=request.POST, instance=request.user)
        picture_form = MyUpdatePictureForm(data=request.POST, files=request.FILES, instance=request.user)
        if data_form.is_valid() and picture_form.is_valid():
            data_form.save()
            picture_form.save()
            messages.success(request, 'Successfully changed  personal data!')
        else:
            for err in data_form.errors.values():
                messages.error(request,str(err))
            for err in picture_form.errors.values():
                messages.error(request,str(err))
    return redirect('edit_profile')

@login_required(login_url='/login/')
def password_change(request):
    if request.method == 'POST':
        form = MyPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Successfully changed  password!')
        else:
            for err in form.errors.values():
                messages.error(request,str(err))
    return redirect('edit_profile')

@login_required(login_url='/login/')
def genres_change(request):
    if request.method == 'POST':
        form = MyChangeGenresForm(data=request.POST, instance=request.user)
        if form.is_valid():
            preferred_genres = form.cleaned_data['preferred_genres']
            genres = Genre.objects.filter(name__in=preferred_genres)
            request.user.preferred_genres.set(genres)
            request.user.save()
            messages.success(request, 'Successfully changed  preferred genres!')
        else:
            error_text = form.errors
            messages.error(request, error_text)
    return redirect('edit_profile')

@login_required(login_url='/login/')
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        password = request.POST.get('password_input')
        if check_password(password, user.password):
            logout(request)
            User.objects.all().filter(id=user.id).delete()
            return redirect('home')
        else:
            messages.error(request, 'Invalid password! Try again!')
    return redirect('edit_profile')

@login_required(login_url='/login/')
def follow_user(request, username):
    follower = request.user
    followed = User.objects.get(username=username)
    follow_relation = FollowRelation(follower=follower, followed=followed)
    follow_relation.save()
    follow_activity = FollowActivity(initiator=follower, followed_user=followed)
    follow_activity.save()
    follow_activity_wrapper = ActivityWrapper(initiator=follower, follow_activity=follow_activity)
    follow_activity_wrapper.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='/login/')
def unfollow_user(request, username):
    follower = request.user
    followed = User.objects.get(username=username)
    FollowRelation.objects.get(follower=follower, followed=followed).delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='/login/')
def read_books(request, username):
    user = User.objects.get(username=username)
    books = ReadBook.objects.filter(user=user).order_by('-read_date')
    books_paginator = Paginator(books, BOOKS_PER_PAGE)
    page_num = request.GET.get('page', 1)
    read_books_page = books_paginator.get_page(page_num)
    return render(request, 'read_books.html',
                  {'user' : user, 'read_books_page' : read_books_page})

@login_required(login_url='/login/')
def currently_reading_books(request, username):
    user = User.objects.get(username=username)
    books = CurrentlyReadingBook.objects.filter(user=user).order_by('-add_date')
    books_paginator = Paginator(books, BOOKS_PER_PAGE)
    page_num = request.GET.get('page', 1)
    currently_reading_page = books_paginator.get_page(page_num)
    return render(request, 'currently_reading_books.html',
                  {'user' : user, 'currently_reading_page' : currently_reading_page})

@login_required(login_url='/login/')
def want_to_read_books(request, username):
    user = User.objects.get(username=username)
    books = WantToReadBook.objects.filter(user=user).order_by('-add_date')
    books_paginator = Paginator(books, BOOKS_PER_PAGE)
    page_num = request.GET.get('page', 1)
    want_to_read_page = books_paginator.get_page(page_num)
    return render(request, 'want_to_read_books.html',
                  {'user' : user, 'want_to_read_page' : want_to_read_page})

@login_required(login_url='/login/')
def reviewed_books(request, username):
    user = User.objects.get(username=username)
    books = BookReview.objects.filter(review_user=user)
    books_paginator = Paginator(books, BOOKS_PER_PAGE)
    page_num = request.GET.get('page', 1)
    reviewed_books_page = books_paginator.get_page(page_num)
    return render(request, 'reviewed_books.html',
                  { 'user' : user, 'reviewed_books_page' : reviewed_books_page})

@login_required(login_url='/login/')
def view_followers(request, username):
    user = User.objects.get(username=username)
    followers = FollowRelation.objects.filter(followed=user)
    followers_paginator = Paginator(followers, ACCOUNTS_PER_PAGE)
    page_num = request.GET.get('page', 1)
    followers_page = followers_paginator.get_page(page_num)
    return render(request, 'followers.html',
                  {'user' : user, 'followers_page' : followers_page})

@login_required(login_url='/login/')
def view_following(request, username):
    user = User.objects.get(username=username)
    following = FollowRelation.objects.filter(follower=user)
    following_paginator = Paginator(following, ACCOUNTS_PER_PAGE)
    page_num = request.GET.get('page', 1)
    following_page = following_paginator.get_page(page_num)
    return render(request, 'following.html',
                  {'user' : user, 'following_page' : following_page})