from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'featured', 'status', 'created']
    list_filter = ['category', 'featured', 'status']
    list_editable = ['category', 'featured', 'status']
    list_per_page = 20

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner']
    list_per_page = 20

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner']
    list_per_page = 20

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['blog', 'name', 'comment', 'date']
    list_per_page = 20
