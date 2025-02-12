from django.urls import reverse
from django.contrib import messages
from django.db.models import Max, Count
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from forum.forms import CreateThreadForm, ThreadReplyForm
from django.contrib.auth.decorators import login_required
from forum.models import Category, Post, Thread, LikeRelation
from activities.models import NewThreadActivity, NewPostActivity, ActivityWrapper


RECENT_FORUM_ACTIVITIES = 50
THREADS_PER_PAGE = 20
POSTS_PER_PAGE = 20


def get_recent_forum_activities():
    thread_activities = ActivityWrapper.objects.filter(new_thread_activity__isnull=False)
    post_activities = ActivityWrapper.objects.filter(new_post_activity__isnull=False)
    recent_activities = (thread_activities | post_activities).order_by('-datetime')[:RECENT_FORUM_ACTIVITIES]
    return recent_activities

@login_required(login_url='/login/')
def show_forum_homepage(request):
    categories = Category.objects.annotate(threads_count=Count('thread')).order_by('name')
    recent_activities = get_recent_forum_activities()
    return render(request, 'forum_homepage.html', { 'categories' : categories,
                                                    'recent_activities' : recent_activities })

@login_required(login_url='/login/')
def show_category(request, slug):
    current_category = Category.objects.get(slug=slug)
    threads = (Thread.objects.filter(category=current_category).annotate(latest_post_time=Max('post__post_datetime'),
                                       posts_count=Count('post')).order_by('-latest_post_time'))
    threads_paginator = Paginator(threads, THREADS_PER_PAGE)
    page_num = request.GET.get('page', 1)
    current_page = threads_paginator.get_page(page_num)
    return render(request, 'category.html', { 'category' : current_category,
                                              'current_page' : current_page })

@login_required(login_url='/login/')
def create_thread(request, slug):
    thread_category = Category.objects.get(slug=slug)
    form = CreateThreadForm()
    return render(request, 'create_thread.html', { 'thread_category' : thread_category,
                                                   'form' : form })

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
    posts = Post.objects.filter(thread=thread).order_by('post_datetime')
    posts_paginator = Paginator(posts, POSTS_PER_PAGE)
    page_num = request.GET.get('page', 1)
    current_page = posts_paginator.get_page(page_num)

    liked_posts_pks = set(LikeRelation.objects.filter(user=request.user, post__in=current_page.object_list).
                          values_list('post_id', flat=True))

    form = ThreadReplyForm()
    return render(request, 'thread.html', {'thread' : thread, 'current_page' : current_page,
                                           'liked_posts_pks' : liked_posts_pks,'form' : form })

@login_required(login_url='/login/')
def add_reply(request, slug):
    user = request.user
    thread = Thread.objects.get(slug=slug)

    if request.method == 'POST':
        form = ThreadReplyForm(request.POST)

        if form.is_valid():
            caption = form.cleaned_data['caption']
            post = Post(author=user, caption=caption, thread=thread)
            post.save()
            new_post_activity = NewPostActivity(initiator=user, thread=thread)
            new_post_activity.save()
            new_post_activity_wrapper = ActivityWrapper(initiator=user,new_post_activity=new_post_activity)
            new_post_activity_wrapper.save()
            messages.success(request, f'Successfully posted in {thread}')

            #redirect the user to the last page where they can see their post
            posts = Post.objects.filter(thread=thread).order_by('post_datetime')
            posts_paginator = Paginator(posts, POSTS_PER_PAGE)
            last_page = posts_paginator.num_pages
            return redirect(f"{reverse('view_thread', args=[slug])}?page={last_page}")

    return redirect('view_thread', slug=thread.slug)\

@login_required(login_url='/login/')
def like_post(request, pk):
    user = request.user
    post = Post.objects.get(pk=pk)
    like = LikeRelation(user=user, post=post)
    like.save()
    messages.success(request, 'Successfully liked a post in the thread!')
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='/login/')
def unlike_post(request, pk):
    user = request.user
    post = Post.objects.get(pk=pk)

    if LikeRelation.objects.filter(user=user, post=post).exists():
        LikeRelation.objects.get(user=user, post=post).delete()
        messages.success(request, 'Successfully unliked a post in the thread!')

    return redirect(request.META.get('HTTP_REFERER', '/'))
