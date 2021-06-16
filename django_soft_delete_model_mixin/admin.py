# -*- coding: utf-8 -*-
from django.contrib import admin

from django_soft_delete_model_mixin.utils import soft_delete_selected


class SoftDeleteModelAdmin(admin.ModelAdmin):
    actions = [soft_delete_selected]  # [SoftDeleteActionView.as_action()]

    def get_actions(self, request):
        actions = super().get_actions(request)
        try:
            actions.pop("delete_selected")
        except KeyError:
            pass
        return actions
