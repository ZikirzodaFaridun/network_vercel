# Generated by Django 5.1.1 on 2025-01-16 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0114_group_group_image_alter_call_room_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call',
            name='room_name',
            field=models.CharField(default='5WzuaZJPwIVs', max_length=100, unique=True),
        ),
    ]
