# -*- coding: utf-8 -*-
import logging

from django.db import models
from django.db.models.signals import pre_delete, post_delete
from django.utils.translation import ugettext_lazy as _

from . import managers as app_managers

logger = logging.getLogger(__name__)


class SoftDeleteModelMixin(models.Model):
    active_objects = app_managers.SoftDeleteModelManager()

    is_removed = models.BooleanField(
        _("Is removed"), default=False, help_text=_("Soft Deleted.")
    )

    class Meta:
        """SoftDeleteModelMixin Meta."""

        abstract = True

    def remove(self, commit=True):
        self.is_removed = True
        if commit:
            self.save()

    remove.alters_data = True

    def delete(self, using=None):
        pre_delete.send(sender=self.__class__, instance=self, using=using)
        self.remove()
        post_delete.send(sender=self.__class__, instance=self, using=using)
        logger.info("Post delete send")

    delete.alters_data = True
