# Generated by Django 3.0 on 2020-05-01 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0011_remove_message_participants'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversation',
            name='user1',
        ),
        migrations.RemoveField(
            model_name='conversation',
            name='user2',
        ),
    ]
