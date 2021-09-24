=====
Usage
=====

To use Soft Delete Model Mixin in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'soft_delete_model_mixin.apps.DjangoSoftDeleteModelMixinConfig',
        ...
    )

Add Soft Delete Model Mixin's URL patterns:

.. code-block:: python

    from soft_delete_model_mixin import urls as soft_delete_model_mixin_urls


    urlpatterns = [
        ...
        url(r'^', include(soft_delete_model_mixin_urls)),
        ...
    ]
