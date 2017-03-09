# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-09 07:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields
import mezzanine.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, verbose_name='Title')),
                ('slug', models.CharField(blank=True, help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL')),
                ('created', models.DateTimeField(editable=False, null=True)),
                ('updated', models.DateTimeField(editable=False, null=True)),
                ('content', mezzanine.core.fields.RichTextField(blank=True, null=True)),
                ('site', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='sites.Site')),
            ],
            options={
                'verbose_name_plural': '分类',
                'verbose_name': '分类',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, verbose_name='Title')),
                ('slug', models.CharField(blank=True, help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL')),
                ('created', models.DateTimeField(editable=False, null=True)),
                ('updated', models.DateTimeField(editable=False, null=True)),
                ('content', mezzanine.core.fields.RichTextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': '公司',
                'verbose_name': '公司',
            },
        ),
        migrations.CreateModel(
            name='GitHubInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
                ('content', mezzanine.core.fields.RichTextField()),
            ],
            options={
                'verbose_name_plural': 'GitHub项目',
                'verbose_name': 'GitHub项目',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keywords_string', models.CharField(blank=True, editable=False, max_length=500)),
                ('_meta_title', models.CharField(blank=True, help_text='Optional title to be used in the HTML title tag. If left blank, the main title field will be used.', max_length=500, null=True, verbose_name='Title')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('gen_description', models.BooleanField(default=True, help_text='If checked, the description will be automatically generated from content. Uncheck if you want to manually set a custom description.', verbose_name='Generate description')),
                ('created', models.DateTimeField(editable=False, null=True)),
                ('updated', models.DateTimeField(editable=False, null=True)),
                ('content', models.TextField(blank=True, verbose_name='内容')),
                ('name', models.CharField(max_length=50, verbose_name='一行介绍')),
                ('province', models.CharField(blank=True, max_length=10, verbose_name='省')),
                ('cities', models.CharField(blank=True, max_length=10, verbose_name='市')),
                ('zone', models.CharField(blank=True, max_length=10, verbose_name='区')),
                ('address', models.CharField(blank=True, max_length=10, verbose_name='地址')),
                ('salary_start', models.IntegerField(blank=True, default=0, verbose_name='待遇（始）')),
                ('salary_end', models.IntegerField(blank=True, default=0, verbose_name='待遇（到）')),
            ],
            options={
                'verbose_name_plural': '工作',
                'verbose_name': '工作',
            },
        ),
        migrations.CreateModel(
            name='Programmer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.CharField(max_length=50)),
                ('blog', models.SlugField()),
                ('company', models.ManyToManyField(blank=True, related_name='company', to='stack.Company', verbose_name='公司')),
            ],
            options={
                'verbose_name_plural': '程序员',
                'verbose_name': '程序员',
            },
        ),
        migrations.CreateModel(
            name='Stack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating_count', models.IntegerField(default=0, editable=False)),
                ('rating_sum', models.IntegerField(default=0, editable=False)),
                ('rating_average', models.FloatField(default=0, editable=False)),
                ('title', models.CharField(max_length=500, verbose_name='Title')),
                ('slug', models.CharField(blank=True, help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL')),
                ('created', models.DateTimeField(editable=False, null=True)),
                ('updated', models.DateTimeField(editable=False, null=True)),
                ('content', mezzanine.core.fields.RichTextField(blank=True, null=True)),
                ('hot', models.IntegerField(blank=True, null=True, verbose_name='热度')),
                ('featured_image', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to='stack')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('category', models.ManyToManyField(blank=True, related_name='category', to='stack.Category', verbose_name='分类')),
                ('site', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='sites.Site')),
            ],
            options={
                'verbose_name_plural': '技术栈',
                'verbose_name': '技术栈',
            },
        ),
        migrations.AddField(
            model_name='programmer',
            name='current_stack',
            field=models.ManyToManyField(blank=True, related_name='current_stack', to='stack.Stack', verbose_name='当前技术栈'),
        ),
        migrations.AddField(
            model_name='programmer',
            name='future_stack',
            field=models.ManyToManyField(blank=True, related_name='future_stack', to='stack.Stack', verbose_name='未来技术栈'),
        ),
        migrations.AddField(
            model_name='programmer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='job',
            name='stacks',
            field=models.ManyToManyField(blank=True, related_name='job_stacks', to='stack.Stack', verbose_name='技术栈'),
        ),
        migrations.AddField(
            model_name='company',
            name='jobs',
            field=models.ManyToManyField(blank=True, related_name='jobs', to='stack.Job', verbose_name='相关工作'),
        ),
        migrations.AddField(
            model_name='company',
            name='site',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='sites.Site'),
        ),
        migrations.AddField(
            model_name='company',
            name='stacks',
            field=models.ManyToManyField(blank=True, related_name='company_stacks', to='stack.Stack', verbose_name='技术栈'),
        ),
    ]
