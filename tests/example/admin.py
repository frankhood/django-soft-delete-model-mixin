from django.contrib import admin

from soft_delete_model_mixin.admin import SoftDeleteModelAdmin
from tests.example.models import Book


@admin.register(Book)
class BookAdmin(SoftDeleteModelAdmin):
    list_display = ("title",)
    fields = ("title",)
