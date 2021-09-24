=============================
Soft Delete Model Mixin
=============================

.. image:: https://badge.fury.io/py/django-soft-delete-model-mixin.svg
    :target: https://badge.fury.io/py/django-soft-delete-model-mixin

.. image:: https://travis-ci.org/frankhood/django-soft-delete-model-mixin.svg?branch=master
    :target: https://travis-ci.org/frankhood/django-soft-delete-model-mixin

.. image:: https://codecov.io/gh/frankhood/django-soft-delete-model-mixin/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/frankhood/django-soft-delete-model-mixin

Use this package if you want a soft delete in your model that remove the entries in your admin but not from the database.

Documentation
-------------

The full documentation is at https://django-soft-delete-model-mixin.readthedocs.io.

Quickstart
----------

Install Soft Delete Model Mixin::

    pip install django-soft-delete-model-mixin

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'soft_delete_model_mixin',
        ...
    )

Add it to your Model:

.. code-block:: python

    from soft_delete_model_mixin import urls as soft_delete_model_mixin_urls

    class Book(SoftDeleteModelMixin, models.Model):
        objects = BookManager.from_queryset(BookQuerySet)()
        title = models.CharField("Title", max_length=255)

        class Meta:
            """Book Meta."""

            verbose_name = "Book"
            verbose_name_plural = "Books"

        def __str__(self):
            return self.title
            
Use it in your Admin:

.. code-block:: python

    @admin.register(Book)
    class BookAdmin(SoftDeleteModelAdmin):
        list_display = ("title",)
        fields = ("title",)

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

::

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
