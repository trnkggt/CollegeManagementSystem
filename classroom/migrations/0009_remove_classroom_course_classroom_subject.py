# Generated by Django 4.2.5 on 2023-11-15 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0014_alter_course_classroom'),
        ('classroom', '0008_classroom_course_alter_classroom_teacher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classroom',
            name='course',
        ),
        migrations.AddField(
            model_name='classroom',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='classrooms', to='courses.subject'),
        ),
    ]
