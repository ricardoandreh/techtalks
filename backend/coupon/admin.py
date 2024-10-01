from coupon.models import Coupon
from django.contrib import admin


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'valid', 'event')
    list_filter = ('valid', 'event')
    search_fields = ('code',)
    ordering = ('event', 'code')

    fieldsets = (
        (None, {
            'fields': ('code', 'discount', 'valid', 'event')
        }),
    )
