# Generated by Django 3.0 on 2020-05-01 13:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0008_message_participants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='participants',
            field=models.ManyToManyField(blank=True, null=True, related_name='conversations', to=settings.AUTH_USER_MODEL),
        ),
    ]
