from typing import Any

from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError

from .models import Category, Husband, Women


@deconstructible
class RussianValidator:
    # Если необходима общая проверка, которая используется многократно.
    ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- '
    code = 'russian'

    def __init__(self, message=None) -> None:
        self.message = message if message else 'Должны присутствовать только русские символы, дефис и пробел.'

    def __call__(self, value, *args: Any, **kwds: Any) -> Any:
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)


class AddPostForm(forms.ModelForm):  # Форма, связанная с моделью
    category = forms.ModelChoiceField(
        label='Категории',
        queryset=Category.objects.all(),
        empty_label='Категория не выбрана',
    )
    husband = forms.ModelChoiceField(
        label='Муж',
        queryset=Husband.objects.all(),
        required=False,
        empty_label='Не замужем',
    )

    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'is_published', 'category', 'husband', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }
        labels = {
            'slug': 'URL'
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')

        return title


# class AddPostForm(forms.Form):  # Форма, не связанная с моделью
#     title = forms.CharField(
#         label='Заголовок',
#         max_length=255,
#         min_length=5,
#         widget=forms.TextInput(attrs={'class': 'form-input'}),
#         # validators=[
#         #     RussianValidator(),
#         # ],
#         error_messages={
#             'min_length': 'Слишком короткий заголовок',
#             'required': 'Без заголовка никак',
#         }
#     )
#     slug = forms.SlugField(
#         label='URL',
#         max_length=255,
#         validators=[
#             MinLengthValidator(5, message='Минимум 5 символов'),
#             MaxLengthValidator(100, message='Максимум 100 символов'),
#         ],
#     )
#     content = forms.CharField(
#         label='Контент',
#         widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}),
#         required=False,
#     )
#     is_published = forms.BooleanField(
#         label='Статус',
#         required=False,
#         initial=True,
#     )
#     category = forms.ModelChoiceField(
#         label='Категории',
#         queryset=Category.objects.all(),
#         empty_label='Категория не выбрана',
#     )
#     husband = forms.ModelChoiceField(
#         label='Муж',
#         queryset=Husband.objects.all(),
#         required=False,
#         empty_label='Не замужем',
#     )

#     def clean_title(self):
#         # Если нужна частная проверка для определенного поля.
#         title = self.cleaned_data['title']
#         ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- '

#         if not (set(title) <= set(ALLOWED_CHARS)):
#             raise ValidationError('Должны присутствовать только русские символы, дефис и пробел.')
