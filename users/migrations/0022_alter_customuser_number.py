# Generated by Django 5.1.1 on 2024-11-15 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_alter_customuser_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='number',
            field=models.PositiveIntegerField(max_length=9),
        ),
    ]
