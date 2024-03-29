from typing import Any
from django.contrib import admin
from django.contrib.admin import ModelAdmin, SimpleListFilter
from django.contrib import messages
from django.db.models.query import QuerySet
from django.utils.safestring import mark_safe

from .models import Women, Category


class MarriedFilter(SimpleListFilter):
    title = 'Статус женщин'
    parameter_name = 'status'

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [
            ('married', 'Замужем'),
            ('single', 'Не замужем'),
        ]

    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(husband__isnull=True)


@admin.register(Women)
class WomenAdmin(ModelAdmin):
    fields = ('title', 'slug', 'content', 'photo', 'post_photo', 'category', 'husband', 'tags')
    # exclude = ('tags', 'is_published')
    # readonly_fields = ('slug', )
    readonly_fields = ('post_photo', )
    prepopulated_fields = {'slug': ('title', )}
    filter_horizontal = ('tags', )
    # filter_vertical = ('tags', )
    list_display = ('title', 'post_photo', 'time_create', 'is_published', 'category')
    list_display_links = ('title', )
    ordering = ['-time_create', 'title']
    list_editable = ('is_published', )
    list_per_page = 5
    actions = ('set_published', 'set_draft')
    search_fields = ('title__startswith', 'category__name')
    list_filter = (MarriedFilter, 'category__name', 'is_published')
    save_on_top = True

    @admin.display(description="Краткое описание", ordering='content')
    def brief_info(self, women: Women):
        return f"Описание {len(women.content)} символов."

    @admin.display(description="Изображение", ordering='content')
    def post_photo(self, women: Women):
        if women.photo:
            return mark_safe(f"<img src='{women.photo.url}' width=50>")
        return 'Без фото'

    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записей.")

    @admin.action(description='Снять с публика выбранные записи')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(
            request,
            f"{count} записей сняты с публикации!",
            messages.WARNING
        )


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
