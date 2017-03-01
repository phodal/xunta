# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 06:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='_profile_following_+', to='user_profile.Profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='birthday',
            field=models.DateTimeField(blank=True, db_index=True, help_text='', null=True, verbose_name='生日'),
        ),
    ]