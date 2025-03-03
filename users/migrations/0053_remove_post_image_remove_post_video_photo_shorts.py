# Generated by Django 5.1.1 on 2024-11-28 13:45

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0052_remove_post_post_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
        migrations.RemoveField(
            model_name='post',
            name='video',
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.TextField(blank=True, max_length=500, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='posts/')),
                ('category', models.CharField(blank=True, choices=[('education', 'Education'), ('entertainment', 'Entertainment'), ('news', 'News'), ('sports', 'Sports')], max_length=50, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Shorts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.TextField(blank=True, max_length=500, null=True)),
                ('video', models.FileField(blank=True, null=True, upload_to='posts/videos/')),
                ('category', models.CharField(blank=True, choices=[('education', 'Education'), ('entertainment', 'Entertainment'), ('news', 'News'), ('sports', 'Sports')], max_length=50, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shorts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
