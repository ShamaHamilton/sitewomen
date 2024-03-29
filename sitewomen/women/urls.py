from django.urls import path, re_path, register_converter

from women.views import *
from women.converters import FourDigitYearConverter

register_converter(FourDigitYearConverter, "year4")

urlpatterns = [
    # path(
    #     '',
    #     WomenHome.as_view(extra_context={'title': 'Главная страница сайта'}),
    #     name='home'
    # ),

    path('',                            WomenHome.as_view(),        name='home'),
    path('addpage/',                    AddPage.as_view(),          name='add_page'),
    path('category/<slug:cat_slug>/',   WomenCategory.as_view(),    name='category'),
    path('tag/<slug:tag_slug>/',        TagPostList.as_view(),      name='tag'),
    path('post/<slug:post_slug>/',      ShowPost.as_view(),         name='post'),
    path('edit/<int:pk>/',              UpdatePage.as_view(),       name='edit_page'),

    # path('',                            index,              name='home'),
    path('about/',                      about,                  name='about'),
    # path('addpage/',                    addpage,            name='add_page'),
    path('contact/',                    contact,                name='contact'),
    path('login/',                      login,                  name='login'),
    # path('post/<slug:post_slug>/',      show_post,              name='post'),
    # path('category/<slug:cat_slug>/',   show_category,          name='category'),
    # path('tag/<slug:tag_slug>/',        show_tag_postlist,      name='tag'),
]
