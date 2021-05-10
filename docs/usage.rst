=====
Usage
=====

To use Soft Delete Model Mixin in a project, add it to your `INSTALLED_APPS`:

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
