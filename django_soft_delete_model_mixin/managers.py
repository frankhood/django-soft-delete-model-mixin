from django.db import models

from .querysets import SoftDeleteQuerySet


class SoftDeleteModelManager(models.Manager):

    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).not_deleted_items()
