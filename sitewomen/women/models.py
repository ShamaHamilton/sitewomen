from django.urls import reverse
from django.db.models import (
    Model, CharField, TextField, DateTimeField, BooleanField, SlugField, Index
)


class Women(Model):
    title = CharField(max_length=255)
    slug = SlugField(max_length=255, unique=True, db_index=True)
    content = TextField(blank=True)
    time_create = DateTimeField(auto_now_add=True)
    time_update = DateTimeField(auto_now=True)
    is_published = BooleanField(default=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['-time_create']
        indexes = [
            Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})
