# Generated by Django 4.2.5 on 2024-02-01 21:11

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0022_remove_studentprofile_enrollement_date"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="studentprofile",
            name="joined_classroom",
        ),
    ]
