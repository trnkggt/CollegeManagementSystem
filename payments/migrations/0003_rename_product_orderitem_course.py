# Generated by Django 4.2.5 on 2023-12-04 11:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_order_paid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='product',
            new_name='course',
        ),
    ]
