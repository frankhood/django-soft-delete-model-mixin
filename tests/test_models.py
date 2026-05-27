from django.db.models.signals import post_delete, pre_delete
from django.test import TestCase

from tests.example.models import Book


class TestSoftDeleteModelMixin(TestCase):
    def test_delete_sets_is_removed(self):
        book = Book.objects.create(title="Test")
        book.delete()
        book.refresh_from_db()
        self.assertTrue(book.is_removed)

    def test_delete_keeps_row_in_db(self):
        book = Book.objects.create(title="Test")
        pk = book.pk
        book.delete()
        self.assertTrue(Book.objects.filter(pk=pk).exists())

    def test_delete_sends_pre_delete_signal(self):
        book = Book.objects.create(title="Test")
        received = []

        def handler(sender, instance, **kwargs):
            received.append(instance)

        pre_delete.connect(handler, sender=Book)
        try:
            book.delete()
        finally:
            pre_delete.disconnect(handler, sender=Book)

        self.assertEqual(len(received), 1)
        self.assertEqual(received[0].pk, book.pk)

    def test_delete_sends_post_delete_signal(self):
        book = Book.objects.create(title="Test")
        received = []

        def handler(sender, instance, **kwargs):
            received.append(instance)

        post_delete.connect(handler, sender=Book)
        try:
            book.delete()
        finally:
            post_delete.disconnect(handler, sender=Book)

        self.assertEqual(len(received), 1)
        self.assertEqual(received[0].pk, book.pk)

    def test_remove_persists(self):
        book = Book.objects.create(title="Test")
        book.remove()
        book.refresh_from_db()
        self.assertTrue(book.is_removed)

    def test_remove_commit_false_does_not_persist(self):
        book = Book.objects.create(title="Test")
        book.remove(commit=False)
        self.assertTrue(book.is_removed)  # in-memory: True
        fresh = Book.objects.get(pk=book.pk)
        self.assertFalse(fresh.is_removed)  # DB unchanged
