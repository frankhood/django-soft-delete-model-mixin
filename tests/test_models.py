#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-soft-delete-model-mixin
------------

Tests for `django-soft-delete-model-mixin` models module.
"""

from django.test import TestCase

from django_soft_delete_model_mixin import models
from tests.example.models import Book


class TestDjangoSoftDeleteModelMixin(TestCase):
    def test_soft_delete(self):
        test_book = Book.objects.create(title="Test")
        test_book.delete()
        test_book.refresh_from_db()
        self.assertTrue(test_book)
        self.assertTrue(test_book.is_removed)
