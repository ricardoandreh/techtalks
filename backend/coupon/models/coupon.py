from django.db import models
from django.utils.translation import gettext_lazy as _
from event.models import Event


class Coupon(models.Model):
    discount = models.DecimalField(
        _("discount"),
        max_digits=5,
        decimal_places=2,
        null=False,
        blank=False,
        help_text=_("The discount amount that the coupon offers."),
    )
    code = models.CharField(
        _("code"),
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        help_text=_("The unique code for redeeming the coupon."),
    )
    valid = models.BooleanField(
        _("valid"),
        default=True,
        help_text=_("Indicates if the coupon is still valid."),
    )
    event = models.ForeignKey(
        Event, 
        on_delete=models.CASCADE,
        related_name="coupons",
        help_text=_("The event with which this coupon is associated."),
    )

    class Meta:
        verbose_name = _("coupon")
        verbose_name_plural = _("coupons")
        ordering = ["event__title"]

    def __str__(self):
        return self.code
