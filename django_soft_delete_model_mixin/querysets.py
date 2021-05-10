from django.db import models


class SoftDeleteQuerySet(models.QuerySet):
    def not_deleted_items(self):
        return self.filter(is_removed=False)

    def deleted_items(self):
        return self.filter(is_removed=True)
