# Generated by Django 4.2.5 on 2023-10-07 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_studentprofile_has_graduated_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='images/student_profiles/'),
        ),
    ]
