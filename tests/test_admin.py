from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import User
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from tests.example.admin import BookAdmin
from tests.example.models import Book


class TestSoftDeleteModelAdminActions(TestCase):
    """Unit tests for SoftDeleteModelAdmin action configuration."""

    def _make_superuser_request(self, path="/"):
        request = RequestFactory().get(path)
        request.user = User(is_superuser=True, is_active=True, is_staff=True)
        return request

    def test_delete_selected_removed_from_actions(self):
        book_admin = BookAdmin(Book, admin.site)
        actions = book_admin.get_actions(self._make_superuser_request())
        self.assertNotIn("delete_selected", actions)

    def test_soft_delete_selected_in_actions(self):
        book_admin = BookAdmin(Book, admin.site)
        actions = book_admin.get_actions(self._make_superuser_request())
        self.assertIn("soft_delete_selected", actions)

    def test_get_queryset_excludes_removed(self):
        """Changelist queryset must hide soft-deleted records."""
        active = Book.objects.create(title="Active")
        removed = Book.objects.create(title="Removed", is_removed=True)
        book_admin = BookAdmin(Book, admin.site)
        qs = book_admin.get_queryset(self._make_superuser_request())
        pks = list(qs.values_list("pk", flat=True))
        self.assertIn(active.pk, pks)
        self.assertNotIn(removed.pk, pks)

    def test_get_queryset_includes_active(self):
        """Changelist queryset must show non-removed records."""
        book = Book.objects.create(title="Visible")
        book_admin = BookAdmin(Book, admin.site)
        qs = book_admin.get_queryset(self._make_superuser_request())
        self.assertIn(book.pk, list(qs.values_list("pk", flat=True)))


class TestSoftDeleteAdminActionFunctional(TestCase):
    """Functional tests for the soft_delete_selected admin action via HTTP."""

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="admin", password="password", email="admin@example.com"
        )
        self.client = Client()
        self.client.login(username="admin", password="password")
        self.book = Book.objects.create(title="Test Book")
        self.changelist_url = reverse("admin:example_book_changelist")

    def _post_action(self, extra=None):
        data = {
            "action": "soft_delete_selected",
            "_selected_action": [str(self.book.pk)],
        }
        if extra:
            data.update(extra)
        return self.client.post(self.changelist_url, data)

    def test_confirmation_page_returns_200(self):
        response = self._post_action()
        self.assertEqual(response.status_code, 200)

    def test_confirmation_page_contains_confirmation_text(self):
        response = self._post_action()
        self.assertContains(response, "Are you sure")

    def test_confirmed_soft_delete_sets_is_removed(self):
        self._post_action({"post": "yes"})
        self.book.refresh_from_db()
        self.assertTrue(self.book.is_removed)

    def test_confirmed_soft_delete_keeps_row_in_db(self):
        self._post_action({"post": "yes"})
        self.assertTrue(Book.objects.filter(pk=self.book.pk).exists())

    def test_confirmed_soft_delete_redirects_to_changelist(self):
        response = self._post_action({"post": "yes"})
        self.assertRedirects(response, self.changelist_url)

    def test_confirmed_soft_delete_creates_log_entry(self):
        self._post_action({"post": "yes"})
        self.assertTrue(
            LogEntry.objects.filter(
                user=self.superuser,
                object_id=str(self.book.pk),
            ).exists()
        )
