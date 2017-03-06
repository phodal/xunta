# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-06 23:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stack', '0010_auto_20170307_0745'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='programmer',
            name='company',
        ),
        migrations.AddField(
            model_name='programmer',
            name='company',
            field=models.ManyToManyField(blank=True, related_name='programmer', to='stack.Company', verbose_name='公司'),
        ),
    ]
