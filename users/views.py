from users.models import User
from django.contrib import messages
from books_database.models import Genre
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from .forms import (MyLoginForm, MyUpdatePictureForm, MySignupForm, MySignupGenresForm, MyEditProfileForm,
                    MyPasswordChangeForm, MyChangeGenresForm)


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
    return render(request, 'user.html', {'user' : user})

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
    user = request.user
    logout(request)
    User.objects.all().filter(id=user.id).delete()
    return redirect('home')