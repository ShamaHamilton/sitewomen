from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import (
    Http404,
    HttpResponse,
    HttpResponseNotFound,
    HttpRequest,
    HttpResponseRedirect,
    HttpResponsePermanentRedirect
)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView
from django.core.paginator import Paginator

from .models import Category, TagPost, Women, UploadFiles
from .forms import AddPostForm, UploadFileForm
from .services import handle_uploaded_file
from .utils import DataMixin


# def index(request: HttpRequest) -> HttpResponse:
#     posts = Women.published.all().select_related('category')  # жадная загрузка

#     data = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0,
#     }
#     return render(request, 'women/index.html', context=data)


class WomenHome(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self) -> QuerySet[Any]:
        return Women.published.all().select_related('category')


def about(request):
    contact_list = Women.published.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'women/about.html', {'title': 'О сайте', 'page_obj': page_obj})

# def about(request):
    # if request.method == 'POST':
    #     form = UploadFileForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         # handle_uploaded_file(form.cleaned_data['file'])
    #         fp = UploadFiles(file=form.cleaned_data['file'])
    #         fp.save()
    # elif request.method == 'GET':
    #     form = UploadFileForm()
    # return render(request, 'women/about.html', {'title': 'О сайте', 'form': form})


class ShowPost(DataMixin, DetailView):
    # model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])

# def addpage(request: HttpRequest) -> HttpResponse:
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # try:  # для форм, не связанных с моделью
#             #     Women.objects.create(**form.cleaned_data)
#             #     return redirect('home')
#             # except:
#             #     form.add_error(None, 'Ошибка добавления поста')
#             # -----------------------------------------------
#             form.save()  # для форм, связанных с моделью
#             return redirect('home')
#     elif request.method == 'GET':
#         form = AddPostForm()

#     data = {
#         'menu': menu,
#         'title': 'Добавление статьи',
#         'form': form
#     }
#     return render(request, 'women/addpage.html', data)


class AddPage(DataMixin, CreateView):
    form_class = AddPostForm
    # model = Women
    # fields = ['title', 'slug', 'content', 'is_published', 'category']
    template_name = 'women/addpage.html'
    # success_url = reverse_lazy('home')  # иначе переходит по get_absolute_url
    title_page = 'Добавление статьи'


# class AddPage(View):
#     def get(self, request):
#         form = AddPostForm()
#         data = {
#             'menu': menu,
#             'title': 'Добавление статьи',
#             'form': form
#         }
#         return render(request, 'women/addpage.html', data)

#     def post(self, request):
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#         data = {
#             'menu': menu,
#             'title': 'Добавление статьи',
#             'form': form
#         }
#         return render(request, 'women/addpage.html', data)


class UpdatePage(DataMixin, UpdateView):
    model = Women
    fields = ['title', 'content', 'photo', 'is_published', 'category']
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')  # иначе переходит по get_absolute_url
    title_page = 'Редактирование статьи'


def contact(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Обратная связь')


def login(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Авторизация')


# def show_category(request: HttpRequest, cat_slug: str) -> HttpResponse:
#     category = get_object_or_404(Category, slug=cat_slug)
#     posts = Women.published.filter(category_id=category.pk).select_related('category')

#     data = {
#         'title': f'Рубрика: {category.name}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': category.pk,
#     }
#     return render(request, 'women/index.html', context=data)


class WomenCategory(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        return Women.published.filter(category__slug=self.kwargs['cat_slug']).select_related('category')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].category
        return self.get_mixin_context(context, title='Категория - ' + cat.name, cat_selected=cat.id)


# def show_tag_postlist(request: HttpRequest, tag_slug: str):
#     tag = get_object_or_404(TagPost, slug=tag_slug)
#     posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('category')
#     data = {
#         'title': f"Тег: {tag.tag}",
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': None,
#     }
#     return render(request, 'women/index.html', data)


class TagPostList(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('category')


def page_not_found(request: HttpRequest, exception) -> HttpResponseNotFound:
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
