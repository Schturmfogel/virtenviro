# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name')),
                ('field_type', models.CharField(max_length=20, verbose_name="Field's data type", choices=[(b'char', 'Char field'), (b'text', 'Text field'), (b'int', 'Integer field'), (b'float', 'Float field'), (b'image', 'Image field')])),
                ('render', models.BooleanField(default=False, verbose_name="Render field's value")),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Additional field',
                'verbose_name_plural': 'Additional fields',
            },
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=250, verbose_name='Title')),
                ('h1', models.CharField(max_length=250, null=True, verbose_name='H1 tag', blank=True)),
                ('intro', models.TextField(null=True, verbose_name='Intro', blank=True)),
                ('content', models.TextField(null=True, verbose_name='Content', blank=True)),
                ('language', models.CharField(default=b'ru', max_length=10, verbose_name='Language', choices=[(b'ru', b'Russian'), (b'en', b'English'), (b'fr', b'France')])),
                ('meta_title', models.CharField(max_length=250, null=True, verbose_name='Meta Title', blank=True)),
                ('meta_keywords', models.TextField(null=True, verbose_name='Meta Keywords', blank=True)),
                ('meta_description', models.TextField(null=True, verbose_name='Meta Description', blank=True)),
                ('published', models.BooleanField(default=False, verbose_name='Published')),
                ('pub_datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created datetime')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last modified datetime')),
                ('author', models.ForeignKey(related_name='created_contents', verbose_name='Author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('last_modified_by', models.ForeignKey(related_name='modified_contents', verbose_name='Corrector', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FieldValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.TextField(verbose_name='Value')),
                ('additional_field', models.ForeignKey(verbose_name='Additional field', to='content.AdditionalField')),
                ('content', models.ForeignKey(verbose_name='Content', to='content.Content')),
            ],
            options={
                'verbose_name': "Additional field's value",
                'verbose_name_plural': "Additional field's values",
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=250, verbose_name='Title')),
                ('slug', models.CharField(unique=True, max_length=60, verbose_name='Slug', blank=True)),
                ('is_home', models.BooleanField(default=False, verbose_name='Is home page')),
                ('published', models.BooleanField(default=False, verbose_name='Published')),
                ('pub_datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created datetime')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last modified datetime')),
                ('ordering', models.IntegerField(default=999999, verbose_name='Ordering')),
                ('login_required', models.BooleanField(default=False, verbose_name='Login required')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('author', models.ForeignKey(related_name='pages', verbose_name='Author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('last_modified_by', models.ForeignKey(related_name='modified_pages', verbose_name='Corrector', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='child_set', verbose_name='Parent', blank=True, to='content.Page', null=True)),
            ],
            options={
                'ordering': ['ordering', '-pub_datetime', 'title'],
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
            },
        ),
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name')),
                ('code', models.TextField(null=True, verbose_name='Code', blank=True)),
                ('render', models.BooleanField(default=False, verbose_name='Render')),
                ('template', models.CharField(max_length=255, null=True, verbose_name='Template', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Snippet',
                'verbose_name_plural': 'Snippets',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(max_length=200, verbose_name='Tag')),
                ('content', models.ManyToManyField(related_name='tags', verbose_name='Content', to='content.Content')),
            ],
            options={
                'ordering': ['tag'],
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('filename', models.CharField(max_length=255, verbose_name='Filename')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(verbose_name='Parent', blank=True, to='content.Template', null=True)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Template',
                'verbose_name_plural': 'Templates',
            },
        ),
        migrations.AddField(
            model_name='page',
            name='template',
            field=models.ForeignKey(verbose_name='Template', to='content.Template'),
        ),
        migrations.AddField(
            model_name='content',
            name='parent',
            field=models.ForeignKey(related_name='contents', verbose_name='Parent', blank=True, to='content.Page', null=True),
        ),
        migrations.AddField(
            model_name='content',
            name='template',
            field=models.ForeignKey(verbose_name='Template', blank=True, to='content.Template', null=True),
        ),
        migrations.AddField(
            model_name='additionalfield',
            name='template',
            field=models.ManyToManyField(related_name='additional_fields', verbose_name='Templates', to='content.Template'),
        ),
        migrations.AlterUniqueTogether(
            name='page',
            unique_together=set([('parent', 'slug')]),
        ),
    ]
