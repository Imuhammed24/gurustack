# Generated by Django 3.0 on 2020-04-09 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0018_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.CharField(blank=True, max_length=95),
        ),
    ]