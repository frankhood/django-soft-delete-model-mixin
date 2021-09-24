# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(
        r"^",
        include(
            "soft_delete_model_mixin.urls",
            namespace="soft_delete_model_mixin",
        ),
    ),
]
