# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-28 13:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0003_auto_20170228_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birthday',
            field=models.DateTimeField(blank=True, db_index=True, help_text='', null=True, verbose_name='生日'),
        ),
    ]
