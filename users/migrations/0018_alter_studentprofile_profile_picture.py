# Generated by Django 4.2.5 on 2023-11-18 15:20

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_alter_studentprofile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='profile_picture',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[150, 150], upload_to='images/student_profiles/'),
        ),
    ]