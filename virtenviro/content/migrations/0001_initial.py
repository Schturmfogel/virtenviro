# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-26 03:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Name')),
                ('field_type', models.CharField(choices=[(b'char', 'Char field'), (b'text', 'Text field'), (b'int', 'Integer field'), (b'float', 'Float field'), (b'image', 'Image field')], max_length=20, verbose_name="Field's data type")),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Title')),
                ('h1', models.CharField(blank=True, max_length=250, null=True, verbose_name='H1 tag')),
                ('intro', models.TextField(blank=True, null=True, verbose_name='Intro')),
                ('content', models.TextField(blank=True, null=True, verbose_name='Content')),
                ('language', models.CharField(choices=[(b'ru', b'Russian'), (b'en', b'English'), (b'fr', b'France')], default=b'ru', max_length=10, verbose_name='Language')),
                ('meta_title', models.CharField(blank=True, max_length=250, null=True, verbose_name='Meta Title')),
                ('meta_keywords', models.TextField(blank=True, null=True, verbose_name='Meta Keywords')),
                ('meta_description', models.TextField(blank=True, null=True, verbose_name='Meta Description')),
                ('published', models.BooleanField(default=False, verbose_name='Published')),
                ('pub_datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created datetime')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last modified datetime')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_contents', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modified_contents', to=settings.AUTH_USER_MODEL, verbose_name='Corrector')),
            ],
        ),
        migrations.CreateModel(
            name='FieldValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField(verbose_name='Value')),
                ('additional_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.AdditionalField', verbose_name='Additional field')),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.Content', verbose_name='Content')),
            ],
            options={
                'verbose_name': "Additional field's value",
                'verbose_name_plural': "Additional field's values",
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('sys_name', models.CharField(max_length=255, verbose_name='System name')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Menu',
                'verbose_name_plural': 'Menus',
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Title')),
                ('slug', models.CharField(blank=True, max_length=250, unique=True, verbose_name='Slug')),
                ('is_home', models.BooleanField(default=False, verbose_name='Is home page')),
                ('is_category', models.BooleanField(default=False, verbose_name='Is category')),
                ('ordering', models.IntegerField(default=999999, verbose_name='Ordering')),
                ('login_required', models.BooleanField(default=False, verbose_name='Login required')),
                ('published', models.BooleanField(default=False, verbose_name='Published')),
                ('pub_datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created datetime')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last modified datetime')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_pages', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modified_pages', to=settings.AUTH_USER_MODEL, verbose_name='Corrector')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_set', to='content.Page', verbose_name='Parent')),
            ],
            options={
                'ordering': ['ordering', '-pub_datetime', 'title'],
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
            },
            managers=[
                ('_default_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='PageMenuRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Title')),
                ('url', models.URLField(blank=True, null=True)),
                ('target', models.CharField(blank=True, choices=[(b'_blank', b'_blank'), (b'_self', b'_self'), (b'_parent', b'_parent'), (b'_top', b'_top')], max_length=15, null=True, verbose_name='Target')),
                ('code', models.TextField(blank=True, null=True, verbose_name='\u041a\u043e\u0434 \u0441\u0441\u044b\u043b\u043a\u0438')),
                ('menu_item_type', models.CharField(choices=[(b'page', '\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u0430'), (b'url', 'URL'), (b'code', '\u041a\u043e\u0434 \u0441\u0441\u044b\u043b\u043a\u0438')], default='page', max_length=25, verbose_name='\u0422\u0438\u043f \u044d\u043b\u0435\u043c\u0435\u043d\u0442\u0430 \u043c\u0435\u043d\u044e')),
                ('ordering', models.IntegerField(default=9999, verbose_name='Ordering')),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.Menu')),
                ('page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='content.Page')),
            ],
            options={
                'ordering': ['menu', 'ordering'],
                'verbose_name': 'Page Menu Relationship',
                'verbose_name_plural': 'Page Menu Relationships',
            },
        ),
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Name')),
                ('code', models.TextField(blank=True, null=True, verbose_name='Code')),
                ('render', models.BooleanField(default=False, verbose_name='Render')),
                ('template', models.CharField(blank=True, max_length=255, null=True, verbose_name='Template')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=200, verbose_name='Tag')),
                ('content', models.ManyToManyField(related_name='tags', to='content.Content', verbose_name='Content')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('filename', models.CharField(max_length=255, verbose_name='Filename')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='content.Template', verbose_name='Parent')),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Template',
                'verbose_name_plural': 'Templates',
            },
            managers=[
                ('_default_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='page',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.Template', verbose_name='Template'),
        ),
        migrations.AddField(
            model_name='menu',
            name='page',
            field=models.ManyToManyField(through='content.PageMenuRelationship', to='content.Page', verbose_name='Page'),
        ),
        migrations.AddField(
            model_name='content',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contents', to='content.Page', verbose_name='Parent'),
        ),
        migrations.AddField(
            model_name='content',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='content.Template', verbose_name='Template'),
        ),
        migrations.AddField(
            model_name='additionalfield',
            name='template',
            field=models.ManyToManyField(related_name='additional_fields', to='content.Template', verbose_name='Templates'),
        ),
        migrations.AlterUniqueTogether(
            name='page',
            unique_together=set([('parent', 'slug')]),
        ),
    ]
