# Generated by Django 5.1.1 on 2024-11-13 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_follow'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follow',
            old_name='followed',
            new_name='following',
        ),
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together={('follower', 'following')},
        ),
    ]
