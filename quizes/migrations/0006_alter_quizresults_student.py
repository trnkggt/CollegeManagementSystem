# Generated by Django 4.2.5 on 2024-02-09 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0025_alter_studentprofile_courses_passed"),
        ("quizes", "0005_quizresults"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quizresults",
            name="student",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="users.studentprofile",
            ),
        ),
    ]
