# Generated by Django 3.0 on 2020-05-05 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0015_auto_20200501_1426'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='messageproperty',
            options={'ordering': ['-timestamp'], 'verbose_name_plural': 'Message Properties'},
        ),
        migrations.AddField(
            model_name='conversation',
            name='last_by',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
