# Generated by Django 5.1.1 on 2024-12-14 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0073_commentstories'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='music',
            field=models.FileField(blank=True, null=True, upload_to='user_music/'),
        ),
    ]
