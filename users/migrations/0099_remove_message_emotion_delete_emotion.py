# Generated by Django 5.1.1 on 2025-01-07 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0098_emotion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='emotion',
        ),
        migrations.DeleteModel(
            name='Emotion',
        ),
    ]
