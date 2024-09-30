from django.db import models
from django.utils.translation import gettext_lazy as _
from organizer.models import Organizer


class Event(models.Model):
    title = models.CharField(
        _("title"),
        max_length=255,
        null=False,
        blank=False,
        help_text=_("The title of the event."),
    )
    description = models.TextField(
        _("description"),
        help_text=_("A detailed description of the event."),
    )
    date = models.DateTimeField(
        _("date"), 
        null=False,
        blank=False,
        help_text=_("The date and time when the event will take place."),
    )
    is_remote = models.BooleanField(
        _("remote"),
        default=False,
        help_text=_("Indicates if the event is remote."),
    )
    event_url = models.URLField(
        _("event URL"), 
        null=True,
        blank=True,
        help_text=_("URL of the event's page."),
    )
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
        help_text=_("The date and time when the event was created."),
    )
    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True,
        help_text=_("The date and time when the event was last updated."),
    )
    organizer = models.ForeignKey(
        Organizer, 
        on_delete=models.CASCADE,
        related_name="events",
        help_text=_("The organizer of the event."),
    )    

    class Meta:
        verbose_name = _("event")
        verbose_name_plural = _("events")
        ordering = ["date"]

    def __str__(self):
        return self.title
