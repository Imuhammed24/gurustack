# Generated by Django 3.0 on 2020-05-01 14:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0013_conversation_participants'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='user1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='conversation_with', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='conversation',
            name='user2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='conversation_from0', to=settings.AUTH_USER_MODEL),
        ),
    ]