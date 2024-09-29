from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .manager import OrganizerManager


class Organizer(AbstractBaseUser, PermissionsMixin):  
    company_name = models.CharField(
        _("company name"), 
        max_length=100, 
        unique=True,
        null=True,
        blank=True,
        error_messages={
            "unique": _("A company with that name already exists."),
        }
    )
    email = models.EmailField(_("email address"), unique=True, null=True, blank=True)
    phone = models.CharField(_("telephone"), max_length=15)
    cnpj = models.CharField(
        "CNPJ",
        max_length=18,
        unique=True,
        null=True,
        blank=True,
        error_messages={
            "unique": _("A company with that CNPJ already exists."),
        }
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = OrganizerManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = _("organizer")
        verbose_name_plural = _("organizers")
        ordering = ["id"]

    def __str__(self):
        return self.company_name or self.email
