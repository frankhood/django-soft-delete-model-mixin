=============================
Soft Delete Model Mixin
=============================

.. image:: https://badge.fury.io/py/django-soft-delete-model-mixin.svg
    :target: https://badge.fury.io/py/django-soft-delete-model-mixin

A Django mixin that implements **soft delete** for your models: calling ``delete()``
marks the record as removed (``is_removed=True``) instead of dropping the row from
the database. The standard Django ``pre_delete`` / ``post_delete`` signals are still
fired, so existing signal handlers keep working without changes.

**Compatibility:** Django 5.2 LTS · Python 3.11 – 3.14

----

Installation
------------

.. code-block:: bash

    pip install django-soft-delete-model-mixin

Add the app to ``INSTALLED_APPS`` in your settings::

    INSTALLED_APPS = [
        ...
        "soft_delete_model_mixin",
        ...
    ]

----

Usage
-----

Model
~~~~~

Inherit from ``SoftDeleteModelMixin`` **before** ``models.Model``.
The mixin adds an ``is_removed`` boolean field and overrides ``delete()``.

.. code-block:: python

    from django.db import models
    from soft_delete_model_mixin.models import SoftDeleteModelMixin
    from soft_delete_model_mixin.managers import SoftDeleteModelManager
    from soft_delete_model_mixin.querysets import SoftDeleteQuerySet


    class BookQuerySet(SoftDeleteQuerySet):
        pass


    class BookManager(SoftDeleteModelManager):
        pass


    class Book(SoftDeleteModelMixin, models.Model):
        # objects  → plain manager (all rows, including removed)
        objects = BookManager.from_queryset(BookQuerySet)()
        title = models.CharField("Title", max_length=255)

        class Meta:
            verbose_name = "Book"
            verbose_name_plural = "Books"

        def __str__(self):
            return self.title

Two managers are available out of the box:

* ``Book.objects`` — all records (your own manager, including removed rows).
* ``Book.active_objects`` — only records where ``is_removed=False``
  (provided by the mixin via ``SoftDeleteModelManager``).

Soft-deleting a record
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    book = Book.objects.get(pk=1)

    # Soft delete: sets is_removed=True, keeps the row, fires pre/post_delete signals
    book.delete()

    # The row still exists in the database
    assert Book.objects.filter(pk=1).exists()          # True
    assert Book.active_objects.filter(pk=1).exists()   # False (hidden)

    # You can also call remove() directly
    book.remove()              # persists immediately (commit=True by default)
    book.remove(commit=False)  # sets is_removed in memory, does NOT save

QuerySet helpers
~~~~~~~~~~~~~~~~

``SoftDeleteQuerySet`` provides two convenience filters:

.. code-block:: python

    Book.objects.not_deleted_items()   # equivalent to filter(is_removed=False)
    Book.objects.deleted_items()       # equivalent to filter(is_removed=True)

Admin
~~~~~

Use ``SoftDeleteModelAdmin`` to replace the default *Delete selected* action with
a soft-delete action that shows a confirmation page before marking items as removed.

.. code-block:: python

    from django.contrib import admin
    from soft_delete_model_mixin.admin import SoftDeleteModelAdmin
    from myapp.models import Book


    @admin.register(Book)
    class BookAdmin(SoftDeleteModelAdmin):
        list_display = ("title",)

The ``delete_selected`` bulk action is automatically removed; the replacement
action ``soft_delete_selected`` is added in its place. Selected records are
marked as ``is_removed=True`` and a Django admin ``LogEntry`` is created for
each one. Records are **not** deleted from the database.

----

Running Tests
-------------

Run the full test suite (requires the package installed in editable mode with
test dependencies)::

    pip install -e ".[test]"
    python runtests.py

Run with coverage::

    coverage run --source soft_delete_model_mixin runtests.py
    coverage report

Run the full tox matrix (Python 3.11 – 3.14 × Django 5.2)::

    tox

----

Manual Testing / Demo
---------------------

The ``tests/`` directory contains a working Django project (``tests.settings``)
with a ``Book`` model that uses the mixin. You can use it to explore the package
behaviour interactively.

.. code-block:: bash

    # 1. Create and activate a virtual environment
    python -m venv .venv
    source .venv/bin/activate          # Windows: .venv\Scripts\activate

    # 2. Install the package with test dependencies
    pip install -e ".[test]"

    # 3. Apply migrations
    python manage.py migrate

    # 4. Create an admin user
    python manage.py createsuperuser

    # 5. Start the development server
    python manage.py runserver

Open http://127.0.0.1:8000/admin/ and log in. Under **Example > Books**:

* Create a few *Book* entries.
* Select one or more, choose **Delete selected Books** from the action dropdown,
  and click **Go**.
* Confirm on the next page — the books disappear from the list but are **not**
  deleted from the database.

Verify from the Django shell::

    python manage.py shell

    >>> from tests.example.models import Book
    >>> Book.objects.count()          # all rows (including soft-deleted)
    >>> Book.active_objects.count()   # only non-removed rows
    >>> Book.objects.filter(is_removed=True).values("title")

----

Development
-----------

Install development tools::

    pip install -r requirements_dev.txt
    invoke -l

Credits
-------

* `Cookiecutter <https://github.com/audreyr/cookiecutter>`_
* `cookiecutter-djangopackage <https://github.com/pydanny/cookiecutter-djangopackage>`_
