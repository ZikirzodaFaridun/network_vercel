# Generated by Django 5.1.1 on 2024-11-13 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_customuser_custom_field_1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='favorite_tv_shows',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='job',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
