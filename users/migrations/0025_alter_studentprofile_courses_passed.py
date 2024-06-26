# Generated by Django 4.2.5 on 2024-02-08 19:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0016_remove_course_classroom"),
        ("users", "0024_coursepassing_studentprofile_courses_passed"),
    ]

    operations = [
        migrations.AlterField(
            model_name="studentprofile",
            name="courses_passed",
            field=models.ManyToManyField(
                related_name="students_passed",
                through="users.CoursePassing",
                to="courses.course",
            ),
        ),
    ]
