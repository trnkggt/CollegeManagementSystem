# Generated by Django 4.2.5 on 2023-11-18 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_studentprofile_joined_classroom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='profile_picture',
            field=models.ImageField(null=True, upload_to='images/student_profiles/'),
        ),
    ]