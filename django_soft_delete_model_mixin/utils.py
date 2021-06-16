from functools import update_wrapper

from django.contrib import messages
from django.contrib.admin import helpers
from django.contrib.admin.models import LogEntry
from django.contrib.admin.utils import get_deleted_objects, model_ngettext
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.db import router
from django.template.response import TemplateResponse
from django.utils.decorators import classonlymethod
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _, ugettext_lazy
from django.views.generic import TemplateView


class AsActionMixin(object):

    short_description = None
    action_name = None

    messages = messages

    @classonlymethod
    def as_action(cls, **initkwargs):
        """
        Main entry point for a request-response process.
        """
        # sanitize keyword arguments
        for key in initkwargs:
            if key in cls.http_method_names:
                raise TypeError(
                    u"You tried to pass in the %s method name as a "
                    u"keyword argument to %s(). Don't do that." % (key, cls.__name__)
                )
            if not hasattr(cls, key):
                raise TypeError(
                    u"%s() received an invalid keyword %r" % (cls.__name__, key)
                )
        initkwargs["action"] = True

        def view(modeladmin, request, queryset, *args, **kwargs):
            self = cls(**initkwargs)
            kwargs.update({"modeladmin": modeladmin, "queryset": queryset})
            # New in django 1.6
            self.request = request
            self.args = args
            self.kwargs = kwargs
            return self.dispatch(request, *args, **kwargs)

        # take name and docstring from class
        update_wrapper(view, cls, updated=())

        # and possible attributes set by decorators
        # like csrf_exempt from dispatch
        update_wrapper(view, cls.dispatch, assigned=())
        if cls.action_name:
            view.__name__ = cls.action_name
        view.short_description = cls.short_description
        return view

    def admin_log(self, obj, change_message, action_flag=None):
        if action_flag == None:
            action_flag = 99
        LogEntry.objects.log_action(
            user_id=self.request.user.pk,
            content_type_id=ContentType.objects.get_for_model(obj).pk,
            object_id=obj.pk,
            object_repr=force_text(obj),
            action_flag=action_flag,
            change_message=change_message,
        )


class SoftDeleteActionView(AsActionMixin, TemplateView):
    template_name = (
        "admin/django_soft_delete_model_mixin/soft_delete_selected_confirmation.html"
    )
    short_description = ugettext_lazy("Delete selected %(verbose_name_plural)s")
    action_name = b"soft_delete_selected"

    # messages = messages

    def do_action(self, modeladmin, request, queryset):
        """
        Default action which deletes the selected objects.

        This action first displays a confirmation page whichs shows all the
        deleteable objects, or, if the user has no permission one of the related
        childs (foreignkeys), a "permission denied" message.

        Next, it deletes all selected objects and redirects back to the change list.
        """
        opts = modeladmin.model._meta
        app_label = opts.app_label

        # Check that the user has delete permission for the actual model
        if not modeladmin.has_delete_permission(request):
            raise PermissionDenied

        using = router.db_for_write(modeladmin.model)

        # Populate deletable_objects, a data structure of all related objects that
        # will also be deleted.
        deletable_objects, model_count, perms_needed, protected = get_deleted_objects(
            queryset, opts, request.user, modeladmin.admin_site, using
        )

        # The user has already confirmed the deletion.
        # Do the deletion and return a None to display the change list view again.
        if request.POST.get("post"):
            if perms_needed:
                raise PermissionDenied
            n = queryset.count()
            if n:
                for obj in queryset:
                    pass
                    # obj_display = force_text(obj)
                    # modeladmin.log_deletion(request, obj, obj_display)
                # queryset.delete()
                for obj in queryset:
                    obj.delete()
                # modeladmin.message_user(request, _("Successfully deleted %(count)d %(items)s.") % {
                #    "count": n, "items": model_ngettext(modeladmin.opts, n)
                # }, messages.SUCCESS)
            # Return None to display the change list page again.
            return None

        if len(queryset) == 1:
            objects_name = force_text(opts.verbose_name)
        else:
            objects_name = force_text(opts.verbose_name_plural)

        if perms_needed or protected:
            title = _("Cannot delete %(name)s") % {"name": objects_name}
        else:
            title = _("Are you sure?")

        context = dict(
            modeladmin.admin_site.each_context(request),
            title=title,
            objects_name=objects_name,
            deletable_objects=[deletable_objects],
            model_count=dict(model_count).items(),
            queryset=queryset,
            perms_lacking=perms_needed,
            protected=protected,
            opts=opts,
            action_checkbox_name=helpers.ACTION_CHECKBOX_NAME,
        )
        request.current_app = modeladmin.admin_site.name
        # print(self.request.current_app)
        return context

    def post(self, request, modeladmin, queryset, **kwargs):
        context = self.do_action(modeladmin, request, queryset, **kwargs)
        return self.render_to_response(context)


def soft_delete_selected(modeladmin, request, queryset):
    """
    Default action which deletes the selected objects.

    This action first displays a confirmation page whichs shows all the
    deleteable objects, or, if the user has no permission one of the related
    childs (foreignkeys), a "permission denied" message.

    Next, it deletes all selected objects and redirects back to the change list.
    """
    opts = modeladmin.model._meta
    app_label = opts.app_label

    # Check that the user has delete permission for the actual model
    if not modeladmin.has_delete_permission(request):
        raise PermissionDenied

    using = router.db_for_write(modeladmin.model)

    # Populate deletable_objects, a data structure of all related objects that
    # will also be deleted.
    # deletable_objects, model_count, perms_needed, protected = get_deleted_objects(
    #     queryset, opts, request.user, modeladmin.admin_site, using)
    deletable_objects, model_count, perms_needed, protected = get_deleted_objects(
        queryset, request, modeladmin.admin_site
    )

    # The user has already confirmed the deletion.
    # Do the deletion and return a None to display the change list view again.
    if request.POST.get("post"):
        if perms_needed:
            raise PermissionDenied
        n = queryset.count()
        if n:
            for obj in queryset:
                obj_display = force_text(obj)
                modeladmin.log_deletion(request, obj, obj_display)
            # queryset.delete()
            for obj in queryset:
                obj.delete()
            modeladmin.message_user(
                request,
                _("Successfully deleted %(count)d %(items)s.")
                % {"count": n, "items": model_ngettext(modeladmin.opts, n)},
                messages.SUCCESS,
            )
        # Return None to display the change list page again.
        return None

    if len(queryset) == 1:
        objects_name = force_text(opts.verbose_name)
    else:
        objects_name = force_text(opts.verbose_name_plural)

    if perms_needed or protected:
        title = _("Cannot delete %(name)s") % {"name": objects_name}
    else:
        title = _("Are you sure?")

    context = dict(
        modeladmin.admin_site.each_context(request),
        title=title,
        objects_name=objects_name,
        deletable_objects=[deletable_objects],
        model_count=dict(model_count).items(),
        queryset=queryset,
        perms_lacking=perms_needed,
        protected=protected,
        opts=opts,
        action_checkbox_name=helpers.ACTION_CHECKBOX_NAME,
    )

    request.current_app = modeladmin.admin_site.name
    # print(request.current_app)
    # Display the confirmation page
    return TemplateResponse(
        request,
        modeladmin.delete_selected_confirmation_template
        or [
            "admin/%s/%s/soft_delete_selected_confirmation.html"
            % (app_label, opts.model_name),
            "admin/%s/soft_delete_selected_confirmation.html" % app_label,
            "admin/django_soft_delete_model_mixin/soft_delete_selected_confirmation.html",
        ],
        context,
    )


soft_delete_selected.short_description = ugettext_lazy(
    "Delete selected %(verbose_name_plural)s"
)
