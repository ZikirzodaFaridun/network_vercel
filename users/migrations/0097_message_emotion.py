# Generated by Django 5.1.1 on 2025-01-07 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0096_videocall'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='emotion',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
