
from django.contrib import admin
from .models import Membership


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = (
        'member',
        'trainer',
        'plan',
        'start_date',
        'end_date',
        'active'
    )

    list_filter = ('active', 'plan')
    search_fields = (
        'member__username',
        'trainer__username',
        'plan'
    )
