# Generated by Django 5.1.1 on 2024-12-21 19:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0083_userpreferences'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserPreferences',
        ),
    ]
