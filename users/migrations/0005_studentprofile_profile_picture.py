# Generated by Django 4.2.5 on 2023-10-05 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_studentprofile_enrolled'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='profile_picture',
            field=models.ImageField(null=True, upload_to='images/student_profiles/'),
        ),
    ]
