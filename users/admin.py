
from django.contrib import admin
from .models import Profile, AuditLog


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone', 'specialty', 'active')
    list_filter = ('role', 'active')
    search_fields = ('user__username', 'user__email')


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'ip_address', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username', 'details', 'action')
    readonly_fields = (
        'user',
        'action',
        'details',
        'ip_address',
        'timestamp'
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
