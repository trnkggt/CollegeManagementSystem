# Generated by Django 4.2.5 on 2023-11-05 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_delete_classroom'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='joined_classroom',
            field=models.BooleanField(default=False),
        ),
    ]
