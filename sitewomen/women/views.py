from django.http import (
    Http404,
    HttpResponse,
    HttpResponseNotFound,
    HttpRequest,
    HttpResponseRedirect,
    HttpResponsePermanentRedirect
)
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string


def index(request: HttpRequest) -> HttpResponse:
    # t = render_to_string('women/index.html')
    # return HttpResponse(t)
    return render(request, 'women/index.html')


def about(request: HttpRequest) -> HttpResponse:
    return render(request, 'women/about.html')


def categories(request: HttpRequest, cat_id: int) -> HttpResponse:
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>id: {cat_id}</p>")


def categories_by_slug(request: HttpRequest, cat_slug: str) -> HttpResponse:
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>slug: {cat_slug}</p>")


def archive(request: HttpRequest, year: int) -> HttpResponse:
    if year > 2024:
        # raise Http404()
        # return redirect('/', permanent=True)
        # return redirect(index)
        # return redirect('home')
        # return redirect('cats', 'music')
        # return HttpResponseRedirect(uri)
        # return HttpResponsePermanentRedirect(uri)

        uri = reverse('cats', args=('music', ))
        return redirect(uri)
    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")


def page_not_found(request: HttpRequest, exception) -> HttpResponseNotFound:
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
