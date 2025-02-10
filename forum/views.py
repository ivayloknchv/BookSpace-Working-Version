from django.contrib import messages
from forum.forms import CreateThreadForm
from django.shortcuts import render, redirect
from forum.models import Category, Post, Thread
from activities.models import NewThreadActivity, ActivityWrapper
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def show_forum_homepage(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'forum_homepage.html', { 'categories' : categories })


@login_required(login_url='/login/')
def show_category(request, slug):
    category = Category.objects.get(slug=slug)
    return render(request, 'category.html', { 'category' : category })

@login_required(login_url='/login/')
def create_thread(request, slug):
    category = Category.objects.get(slug=slug)
    form = CreateThreadForm()
    return render(request, 'create_thread.html', { 'category' : category, 'form' : form })

@login_required(login_url='/login/')
def save_thread(request, slug):
    user = request.user
    category = Category.objects.get(slug=slug)

    if request.method == 'POST':
        form = CreateThreadForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            caption = form.cleaned_data['caption']
            thread = Thread(author=user, title=title, category=category)
            thread.save()
            post = Post(author=user, thread=thread, caption=caption)
            post.save()
            new_thread_activity = NewThreadActivity(initiator=user, thread=thread)
            new_thread_activity.save()
            new_thread_activity_wrapper = ActivityWrapper(initiator=user, new_thread_activity=new_thread_activity)
            new_thread_activity_wrapper.save()
            messages.success(request, 'Successfully created a new thread in the forum')
            return redirect('view_thread', slug=thread.slug)

@login_required(login_url='/login/')
def view_thread(request, slug):
    thread = Thread.objects.get(slug=slug)
    return render(request, 'thread.html', {'thread' : thread })