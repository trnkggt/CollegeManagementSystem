# Generated by Django 4.2.5 on 2023-10-05 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_customuser_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='enrolled',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
