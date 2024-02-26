from django.db.models.query import QuerySet
from django.urls import reverse
from django.db.models import (
    Model, Index, Manager, IntegerChoices,
    CharField, TextField, DateTimeField, BooleanField, SlugField, IntegerField,
    ForeignKey, ManyToManyField, OneToOneField, PROTECT, SET_NULL
)


class PublishedManager(Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class Women(Model):
    class Status(IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = CharField(max_length=255, verbose_name='Заголовок')
    slug = SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug')
    content = TextField(blank=True, verbose_name='Текст статьи')
    time_create = DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                default=Status.DRAFT,
                                verbose_name='Статус')
    category = ForeignKey('Category', on_delete=PROTECT, related_name='posts',
                          verbose_name='Категории')  # women_set -> posts
    tags = ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name='Теги')
    husband = OneToOneField('Husband', on_delete=SET_NULL, null=True,
                            blank=True, related_name='wuman', verbose_name='Муж')

    objects = Manager()
    published = PublishedManager()

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Известные женщины'
        verbose_name_plural = 'Известные женщины'

        ordering = ['-time_create']
        indexes = [
            Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


class Category(Model):
    name = CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class TagPost(Model):
    tag = CharField(max_length=100, db_index=True)
    slug = SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self) -> str:
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class Husband(Model):
    name = CharField(max_length=100)
    age = IntegerField(null=True)

    def __str__(self) -> str:
        return self.name
