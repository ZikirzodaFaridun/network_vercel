# Generated by Django 5.1.1 on 2025-01-07 05:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0093_delete_videocall'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoCall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('ended_at', models.DateTimeField(blank=True, null=True)),
                ('chat', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='video_call', to='users.chat')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hosted_calls', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
