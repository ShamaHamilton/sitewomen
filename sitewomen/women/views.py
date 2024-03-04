from django.http import (
    Http404,
    HttpResponse,
    HttpResponseNotFound,
    HttpRequest,
    HttpResponseRedirect,
    HttpResponsePermanentRedirect
)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string

from .models import Category, TagPost, Women, UploadFiles
from .forms import AddPostForm, UploadFileForm
from .services import handle_uploaded_file

menu = [
    {'title': 'О сайте',            'url_name': 'about'},
    {'title': 'Добавить статью',    'url_name': 'add_page'},
    {'title': 'Обратная связь',     'url_name': 'contact'},
    {'title': 'Войти',              'url_name': 'login'},
]


def index(request: HttpRequest) -> HttpResponse:
    posts = Women.published.all().select_related('category')  # жадная загрузка

    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'women/index.html', context=data)


def about(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # handle_uploaded_file(form.cleaned_data['file'])
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    elif request.method == 'GET':
        form = UploadFileForm()
    return render(request, 'women/about.html', {'title': 'О сайте', 'menu': menu, 'form': form})


def show_post(request: HttpRequest, post_slug: int) -> HttpResponse:
    post = get_object_or_404(Women, slug=post_slug)

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }
    return render(request, 'women/post.html', data)


def addpage(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            # print(form.cleaned_data)
            # try:  # для форм, не связанных с моделью
            #     Women.objects.create(**form.cleaned_data)
            #     return redirect('home')
            # except:
            #     form.add_error(None, 'Ошибка добавления поста')
            # -----------------------------------------------
            form.save()  # для форм, связанных с моделью
            return redirect('home')
    elif request.method == 'GET':
        form = AddPostForm()

    data = {
        'menu': menu,
        'title': 'Добавление статьи',
        'form': form
    }
    return render(request, 'women/addpage.html', data)


def contact(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Обратная связь')


def login(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Авторизация')


def show_category(request: HttpRequest, cat_slug: str) -> HttpResponse:
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.filter(category_id=category.pk).select_related('category')

    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'women/index.html', context=data)


def show_tag_postlist(request: HttpRequest, tag_slug: str):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('category')
    data = {
        'title': f"Тег: {tag.tag}",
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }
    return render(request, 'women/index.html', data)


def page_not_found(request: HttpRequest, exception) -> HttpResponseNotFound:
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
