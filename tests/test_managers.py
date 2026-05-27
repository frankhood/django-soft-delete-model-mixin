from django.test import TestCase

from tests.example.models import Book


class TestSoftDeleteModelManager(TestCase):
    def setUp(self):
        self.active_book = Book.objects.create(title="Active")
        self.removed_book = Book.objects.create(title="Removed")
        self.removed_book.delete()

    def test_active_objects_excludes_removed(self):
        self.assertNotIn(self.removed_book, Book.active_objects.all())

    def test_active_objects_includes_non_removed(self):
        self.assertIn(self.active_book, Book.active_objects.all())

    def test_objects_includes_all(self):
        self.assertIn(self.active_book, Book.objects.all())
        self.assertIn(self.removed_book, Book.objects.all())

    def test_delete_decrements_active_objects_count(self):
        book = Book.objects.create(title="New")
        count_before = Book.active_objects.count()
        book.delete()
        self.assertEqual(Book.active_objects.count(), count_before - 1)

    def test_delete_does_not_change_objects_count(self):
        book = Book.objects.create(title="New")
        count_before = Book.objects.count()
        book.delete()
        self.assertEqual(Book.objects.count(), count_before)
