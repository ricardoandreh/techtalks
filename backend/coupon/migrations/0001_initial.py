# Generated by Django 5.1.1 on 2024-10-01 02:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("event", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Coupon",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "discount",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="The discount amount that the coupon offers.",
                        max_digits=5,
                        verbose_name="discount",
                    ),
                ),
                (
                    "code",
                    models.CharField(
                        help_text="The unique code for redeeming the coupon.",
                        max_length=255,
                        unique=True,
                        verbose_name="code",
                    ),
                ),
                (
                    "valid",
                    models.BooleanField(
                        default=True, help_text="Indicates if the coupon is still valid.", verbose_name="valid"
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        help_text="The event with which this coupon is associated.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="coupons",
                        to="event.event",
                    ),
                ),
            ],
            options={
                "verbose_name": "coupon",
                "verbose_name_plural": "coupons",
            },
        ),
    ]
