
from .models import AuditLog


def get_client_ip(request):
    return request.META.get('REMOTE_ADDR')


def log_action(request, action, details=''):
    AuditLog.objects.create(
        user=request.user if request.user.is_authenticated else None,
        action=action,
        details=details,
        ip_address=get_client_ip(request)
    )
