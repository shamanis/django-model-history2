from django.conf import settings
from django.contrib import admin, messages
from django.utils.translation import ugettext_lazy as _
from .models import History

MODEL_HISTORY_SETTINGS = getattr(settings, 'MODEL_HISTORY_SETTINGS', {})


class HisotryAdmin(admin.ModelAdmin):
    list_display = ['created_date', 'user', 'model', 'object', 'type', 'status', 'field', 'old_value', 'new_value']
    list_filter = ['type', 'status']
    readonly_fields = ['created_date', 'user', 'model', 'object', 'type', 'status',
                       'field', 'old_value', 'new_value', 'dump']
    date_hierarchy = 'created_date'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        delete_permission = MODEL_HISTORY_SETTINGS.get('delete_permission', None)
        if delete_permission and getattr(request.user, delete_permission, False):
            return True
        return False

    def get_actions(self, request):
        actions = super(HisotryAdmin, self).get_actions(request)
        delete_action = MODEL_HISTORY_SETTINGS.get('delete_action', False)
        revert_action = MODEL_HISTORY_SETTINGS.get('revert_action', True)
        if not delete_action:
            if 'delete_selected' in actions:
                del actions['delete_selected']

        if revert_action:
            self.actions.append('revert')
        return actions

    def revert(self, request, queryset):
        revert_permission = MODEL_HISTORY_SETTINGS.get('revert_permission', None)
        if revert_permission and not getattr(request.user, revert_permission, False):
            self.message_user(request, _('You have not permission for reverted objects'), level=messages.ERROR)
            return

        all_count, reverted_count = 0, 0
        for history in queryset:
            if history.revert():
                reverted_count += 1
            else:
                self.message_user(request, _('The object can not be reverted. Perhaps it was changed later.'),
                                  level=messages.WARNING)
                return

            all_count += 1
        self.message_user(request, _('%d of %d reverted') % (reverted_count, all_count))
    revert.short_description = _('Revert')


admin.site.register(History, HisotryAdmin)