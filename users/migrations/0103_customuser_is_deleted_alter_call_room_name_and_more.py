# Generated by Django 5.1.1 on 2025-01-11 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0102_call'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='call',
            name='room_name',
            field=models.CharField(default='O4sOKKDTwTW9', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
