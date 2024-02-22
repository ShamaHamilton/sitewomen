from django.db.models.query import QuerySet
from django.urls import reverse
from django.db.models import (
    Model, Index, Manager, IntegerChoices,
    CharField, TextField, DateTimeField, BooleanField, SlugField,
    ForeignKey, ManyToManyField, PROTECT
)


class PublishedManager(Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class Women(Model):
    class Status(IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = CharField(max_length=255)
    slug = SlugField(max_length=255, unique=True, db_index=True)
    content = TextField(blank=True)
    time_create = DateTimeField(auto_now_add=True)
    time_update = DateTimeField(auto_now=True)
    is_published = BooleanField(choices=Status.choices, default=Status.DRAFT)
    category = ForeignKey('Category', on_delete=PROTECT, related_name='posts')  # women_set -> posts
    tags = ManyToManyField('TagPost', blank=True, related_name='tags')

    objects = Manager()
    published = PublishedManager()

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['-time_create']
        indexes = [
            Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


class Category(Model):
    name = CharField(max_length=100, db_index=True)
    slug = SlugField(max_length=255, unique=True, db_index=True)

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
