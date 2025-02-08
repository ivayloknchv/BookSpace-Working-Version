from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from forum.models import Category, Thread


@login_required(login_url='/login/')
def show_forum_homepage(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'forum_homepage.html', { 'categories' : categories })


@login_required(login_url='/login/')
def show_category(request, slug):
    category = Category.objects.get(slug=slug)
    return render(request, 'category.html', { 'category' : category})