# Generated by Django 3.0 on 2020-05-01 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0014_auto_20200501_1424'),
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
