# Generated by Django 4.2.5 on 2023-10-19 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_course_code_course_credits'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='code',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
    ]
