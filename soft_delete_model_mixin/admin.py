from django.contrib import admin

from soft_delete_model_mixin.utils import soft_delete_selected


class SoftDeleteModelAdmin(admin.ModelAdmin):
    actions = [soft_delete_selected]  # [SoftDeleteActionView.as_action()]

    def get_queryset(self, request):
        """Return only non-removed objects in the changelist."""
        qs = self.model._default_manager.all()
        if hasattr(qs, "not_deleted_items"):
            return qs.not_deleted_items()
        if hasattr(self.model, "active_objects"):
            return self.model.active_objects.all()
        return qs

    def get_actions(self, request):
        actions = super().get_actions(request)
        try:
            actions.pop("delete_selected")
        except KeyError:
            pass
        return actions
