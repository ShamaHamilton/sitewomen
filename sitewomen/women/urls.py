from django.urls import path, re_path, register_converter

from women.views import *
from women.converters import FourDigitYearConverter

register_converter(FourDigitYearConverter, "year4")

urlpatterns = [
    path('', index),
    path('cats/<int:cat_id>/', categories),
    path('cats/<slug:cat_slug>/', categories_by_slug),
    # re_path(r"^archive/(?P<year>[0-9]{4})/", archive),
    path('archive/<year4:year>/', archive),
]
