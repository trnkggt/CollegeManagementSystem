# Generated by Django 4.2.5 on 2023-10-13 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_customuser_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='experience',
            field=models.TextField(blank=True, null=True),
        ),
    ]
