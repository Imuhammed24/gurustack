# Generated by Django 3.0 on 2020-05-01 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0010_auto_20200501_1348'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='participants',
        ),
    ]
