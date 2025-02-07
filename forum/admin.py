from django.contrib import admin
from forum.models import Category


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    ordering = ('name', 'description', 'slug')
    fields = ('name', 'description', 'slug')
    list_display = ('name', 'description', 'slug')


admin.site.register(Category, CategoryAdmin)
