# Generated by Django 5.1.1 on 2025-01-16 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0113_remove_shorts_low_res_video_alter_call_room_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='group_image',
            field=models.ImageField(blank=True, null=True, upload_to='groups/pictures'),
        ),
        migrations.AlterField(
            model_name='call',
            name='room_name',
            field=models.CharField(default='snwNn8hwWz3R', max_length=100, unique=True),
        ),
    ]
