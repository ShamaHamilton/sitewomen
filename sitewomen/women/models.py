from transliterate import translit

from django.db.models.query import QuerySet
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator


class PublishedManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class Women(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(
        verbose_name='Заголовок',
        max_length=255,
    )
    slug = models.SlugField(
        verbose_name='Slug',
        max_length=255,
        unique=True,
        db_index=True,
        validators=[
            MinLengthValidator(5, message='Минимум 5 символов'),
            MaxLengthValidator(100, message='Максимум 100 символов'),
        ],
    )
    photo = models.ImageField(
        verbose_name='Фото',
        upload_to='photos/%Y/%m/%d/',
        default=None,
        blank=True,
        null=True,
    )
    content = models.TextField(
        verbose_name='Текст статьи',
        blank=True,
    )
    time_create = models.DateTimeField(
        verbose_name='Время создания',
        auto_now_add=True,
    )
    time_update = models.DateTimeField(
        verbose_name='Время изменения',
        auto_now=True,
    )
    is_published = models.BooleanField(
        verbose_name='Статус',
        choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
        default=Status.DRAFT,
    )
    category = models.ForeignKey(
        verbose_name='Категории',
        to='Category',
        on_delete=models.PROTECT,
        related_name='posts',  # women_set -> posts
    )
    tags = models.ManyToManyField(
        verbose_name='Теги',
        to='TagPost',
        blank=True,
        related_name='tags',
    )
    husband = models.OneToOneField(
        verbose_name='Муж',
        to='Husband',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='wuman',
    )

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Известные женщины'
        verbose_name_plural = 'Известные женщины'

        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    # def save(self, *args, **kwargs) -> None:
    #     self.slug = slugify(translit(self.title, 'ru', reversed=True))
    #     super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(
        verbose_name='Категория',
        max_length=100,
        db_index=True,
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class TagPost(models.Model):
    tag = models.CharField(
        max_length=100,
        db_index=True,
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
    )

    def __str__(self) -> str:
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class Husband(models.Model):
    name = models.CharField(
        max_length=100
    )
    age = models.IntegerField(
        null=True
    )

    def __str__(self) -> str:
        return self.name


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')
