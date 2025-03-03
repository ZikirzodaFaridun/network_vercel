# Generated by Django 5.1.1 on 2024-12-06 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0059_story_delete_flashtop'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='story',
            options={'ordering': ['-created_at']},
        ),
        migrations.RenameField(
            model_name='story',
            old_name='media',
            new_name='content',
        ),
        migrations.RemoveField(
            model_name='story',
            name='caption',
        ),
        migrations.RemoveField(
            model_name='story',
            name='is_active',
        ),
        migrations.AlterField(
            model_name='story',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
