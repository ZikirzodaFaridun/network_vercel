# Generated by Django 5.1.1 on 2024-11-13 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_customuser_custom_field_1_customuser_custom_field_2_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='custom_field_1',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='custom_field_2',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='custom_field_3',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='custom_field_4',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='custom_field_5',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='favorite_tv_shows',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='job',
        ),
    ]
