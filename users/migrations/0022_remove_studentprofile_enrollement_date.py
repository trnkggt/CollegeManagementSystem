# Generated by Django 4.2.5 on 2024-02-01 21:08

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0021_remove_studentprofile_has_paid"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="studentprofile",
            name="enrollement_date",
        ),
    ]
