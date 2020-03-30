# Generated by Django 3.0 on 2020-03-28 11:11

import taggit_selectize.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('account', '0016_auto_20200326_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='interests',
            field=taggit_selectize.managers.TaggableManager(help_text='football, programming, photography', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Interests'),
        ),
    ]