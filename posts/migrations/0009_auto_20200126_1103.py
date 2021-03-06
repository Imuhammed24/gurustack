# Generated by Django 3.0 on 2020-01-26 11:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0008_post_users_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='users_like',
            field=models.ManyToManyField(blank=True, related_name='posts_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
