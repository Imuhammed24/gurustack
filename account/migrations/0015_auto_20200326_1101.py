# Generated by Django 3.0 on 2020-03-26 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_profile_email_confirmed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
