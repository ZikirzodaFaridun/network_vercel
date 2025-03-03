# Generated by Django 5.1.1 on 2025-01-11 20:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0106_remove_customuser_is_deleted_alter_call_room_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='blocked_users',
            field=models.ManyToManyField(blank=True, related_name='blocked_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='call',
            name='room_name',
            field=models.CharField(default='SMz0eVPPDPyv', max_length=100, unique=True),
        ),
    ]
