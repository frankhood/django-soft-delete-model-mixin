from django.db import models

from django_soft_delete_model_mixin.models import SoftDeleteModelMixin
from tests.example.managers import BookManager
from tests.example.querysets import BookQuerySet


class Book(SoftDeleteModelMixin, models.Model):
    objects = BookManager.from_queryset(BookQuerySet)()
    title = models.CharField("Title", max_length=255)

    class Meta:
        """Book Meta."""

        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return self.title
