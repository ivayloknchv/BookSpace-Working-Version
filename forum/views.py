from django.db.models import Max, Count
from django.contrib import messages
from forum.forms import CreateThreadForm
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from forum.models import Category, Post, Thread
from django.contrib.auth.decorators import login_required
from activities.models import NewThreadActivity, NewPostActivity, ActivityWrapper


RECENT_FORUM_ACTIVITIES = 50
THREADS_PER_PAGE = 20


def get_recent_forum_activities():
    thread_activites = ActivityWrapper.objects.filter(new_thread_activity__isnull=False)
    post_activites = ActivityWrapper.objects.filter(new_post_activity__isnull=False)
    recent_activities = (thread_activites | post_activites).order_by('-datetime')[:RECENT_FORUM_ACTIVITIES]
    return recent_activities

@login_required(login_url='/login/')
def show_forum_homepage(request):
    categories = Category.objects.annotate(threads_count=Count('thread')).order_by('name')
    recent_activities = get_recent_forum_activities()
    return render(request, 'forum_homepage.html', { 'categories' : categories,
                                                    'recent_activities' : recent_activities })

@login_required(login_url='/login/')
def show_category(request, slug):
    category = Category.objects.get(slug=slug)
    threads = (Thread.objects.filter(category=category).annotate(latest_post_time=Max('post__post_datetime'),
                                       posts_count=Count('post')).order_by('-latest_post_time'))
    threads_paginator = Paginator(threads, THREADS_PER_PAGE)
    page_num = request.GET.get('page', 1)
    current_page = threads_paginator.get_page(page_num)
    return render(request, 'category.html', { 'category' : category,
                                              'current_page' : current_page })

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