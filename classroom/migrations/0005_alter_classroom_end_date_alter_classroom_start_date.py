# Generated by Django 4.2.5 on 2023-11-15 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0004_alter_classroom_end_date_alter_classroom_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='end_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='classroom',
            name='start_date',
            field=models.DateTimeField(),
        ),
    ]