from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Women, Category


@admin.register(Women)
class WomenAdmin(ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'is_published', 'category')
    list_display_links = ('id', 'title')
    ordering = ['-time_create', 'title']
    list_editable = ('is_published',)
    list_per_page = 5


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
