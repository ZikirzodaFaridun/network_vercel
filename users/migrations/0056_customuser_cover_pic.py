# Generated by Django 5.1.1 on 2024-12-05 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0055_remove_customuser_favorite_tv_shows_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='cover_pic',
            field=models.ImageField(blank=True, null=True, upload_to='cover_pics/'),
        ),
    ]
