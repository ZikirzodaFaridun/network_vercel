# Generated by Django 5.1.1 on 2025-01-16 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0111_alter_call_room_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='shorts',
            name='low_res_video',
            field=models.FileField(blank=True, null=True, upload_to='videos/low_res/'),
        ),
        migrations.AlterField(
            model_name='call',
            name='room_name',
            field=models.CharField(default='NvJGubOiArbD', max_length=100, unique=True),
        ),
    ]
