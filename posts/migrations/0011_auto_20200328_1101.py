# Generated by Django 3.0 on 2020-03-28 11:01

import taggit_selectize.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('posts', '0010_auto_20200328_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='tags',
            field=taggit_selectize.managers.TaggableManager(blank=True, help_text=None, through='taggit.TaggedItem', to='taggit.Tag', verbose_name=''),
        ),
    ]
