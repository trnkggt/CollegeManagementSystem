# Generated by Django 4.2.5 on 2023-10-22 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_classroom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='student_count',
            field=models.PositiveIntegerField(),
        ),
    ]