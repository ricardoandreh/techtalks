# Generated by Django 5.1.1 on 2024-09-28 23:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("organizer", "0006_alter_organizer_cnpj"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="organizer",
            options={"ordering": ["id"], "verbose_name": "organizer", "verbose_name_plural": "organizers"},
        ),
    ]
