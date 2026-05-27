from django.test import TestCase

from soft_delete_model_mixin.querysets import SoftDeleteQuerySet
from tests.example.models import Book


class TestSoftDeleteQuerySet(TestCase):
    def setUp(self):
        self.active = Book.objects.create(title="Active")
        self.removed = Book.objects.create(title="Removed", is_removed=True)

    def test_not_deleted_items_returns_only_active(self):
        qs = SoftDeleteQuerySet(
            model=Book, using="default"
        ).not_deleted_items()
        pks = list(qs.values_list("pk", flat=True))
        self.assertIn(self.active.pk, pks)
        self.assertNotIn(self.removed.pk, pks)

    def test_deleted_items_returns_only_removed(self):
        qs = SoftDeleteQuerySet(model=Book, using="default").deleted_items()
        pks = list(qs.values_list("pk", flat=True))
        self.assertIn(self.removed.pk, pks)
        self.assertNotIn(self.active.pk, pks)

    def test_not_deleted_items_count(self):
        qs = SoftDeleteQuerySet(
            model=Book, using="default"
        ).not_deleted_items()
        self.assertEqual(qs.count(), 1)

    def test_deleted_items_count(self):
        qs = SoftDeleteQuerySet(model=Book, using="default").deleted_items()
        self.assertEqual(qs.count(), 1)
