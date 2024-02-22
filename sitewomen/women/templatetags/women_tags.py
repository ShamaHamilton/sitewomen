from django import template
from django.db.models import Count

from women.models import Category, TagPost


register = template.Library()


@register.inclusion_tag('women/list_categories.html')
def show_categories(cat_selected: int = 0):
    # cats = Category.objects.all()
    cats = Category.objects.annotate(total=Count("posts")).filter(total__gt=0)
    return {'cats': cats, 'cat_selected': cat_selected}


@register.inclusion_tag('women/list_tags.html')
def show_all_tags():
    # return {'tags': TagPost.objects.all()}
    return {'tags': TagPost.objects.annotate(total=Count("tags")).filter(total__gt=0)}
