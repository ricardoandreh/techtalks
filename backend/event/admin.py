from django.contrib import admin
from event.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "organizer", "is_remote")
    search_fields = ("title", "description")
    list_filter = ("date", "is_remote", "organizer")
    ordering = ("date",)
