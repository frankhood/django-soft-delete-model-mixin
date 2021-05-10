# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views


app_name = 'django_soft_delete_model_mixin'
urlpatterns = [
    url(r'', TemplateView.as_view(template_name="base.html")),
    ]
