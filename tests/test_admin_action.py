from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tests.example.models import Book


class TestSoftDeleteAdminAction(TestCase):
    def setUp(self):
        User = get_user_model()
        self.admin_user = User.objects.create_superuser("admin", "admin@example.com", "pass")
        self.client.force_login(self.admin_user)

    def test_soft_delete_selected_action(self):
        book = Book.objects.create(title="Test")
        url = reverse("admin:example_book_changelist")
        response = self.client.post(
            url,
            {
                "action": "soft_delete_selected",
                "_selected_action": [str(book.pk)],
                "post": "yes",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        book.refresh_from_db()
        self.assertTrue(book.is_removed)
