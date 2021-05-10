=============================
Soft Delete Model Mixin
=============================

.. image:: https://badge.fury.io/py/django-soft-delete-model-mixin.svg
    :target: https://badge.fury.io/py/django-soft-delete-model-mixin

.. image:: https://travis-ci.org/frankhood/django-soft-delete-model-mixin.svg?branch=master
    :target: https://travis-ci.org/frankhood/django-soft-delete-model-mixin

.. image:: https://codecov.io/gh/frankhood/django-soft-delete-model-mixin/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/frankhood/django-soft-delete-model-mixin

A Soft delete model mixin for your Django Model

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
        'django_soft_delete_model_mixin.apps.DjangoSoftDeleteModelMixinConfig',
        ...
    )

Add Soft Delete Model Mixin's URL patterns:

.. code-block:: python

    from django_soft_delete_model_mixin import urls as django_soft_delete_model_mixin_urls


    urlpatterns = [
        ...
        url(r'^', include(django_soft_delete_model_mixin_urls)),
        ...
    ]

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
