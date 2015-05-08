# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', models.CharField(max_length=60, null=True, verbose_name='Slug', blank=True)),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('image', models.ImageField(upload_to='H:/GITHUB/virtenviro\\..\\media\\img\\shop\\category', null=True, verbose_name='Image', blank=True)),
                ('meta_title', models.CharField(max_length=250, null=True, verbose_name='Meta Title', blank=True)),
                ('meta_keywords', models.TextField(null=True, verbose_name='Meta Keywords', blank=True)),
                ('meta_description', models.TextField(null=True, verbose_name='Meta Description', blank=True)),
                ('ordering', models.IntegerField(default=0, null=True, verbose_name='Ordering', blank=True)),
                ('view_count', models.IntegerField(default=0, null=True, verbose_name='Count of views', blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='subcategories', verbose_name='Parent', blank=True, to='shop.Category', null=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='Currency')),
                ('default', models.BooleanField(default=False, verbose_name='Is default currency')),
                ('symbol', models.CharField(max_length=10, null=True, verbose_name='Symbol', blank=True)),
                ('char_code', models.CharField(max_length=10, null=True, verbose_name='Char code of currency', blank=True)),
                ('num_code', models.IntegerField(null=True, verbose_name='Code of currency', blank=True)),
                ('nominal', models.FloatField(null=True, verbose_name='Nominal', blank=True)),
                ('value', models.FloatField(null=True, verbose_name='Value', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Currency',
                'verbose_name_plural': 'Currencies',
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', filebrowser.fields.FileBrowseField(max_length=200, null=True, verbose_name=b'File', blank=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Name', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', filebrowser.fields.FileBrowseField(max_length=200, null=True, verbose_name=b'Image', blank=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Name', blank=True)),
                ('is_main', models.BooleanField(default=False, verbose_name='Is Main')),
            ],
            options={
                'ordering': ['image_type', 'name'],
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
            },
        ),
        migrations.CreateModel(
            name='ImageType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Images Type',
                'verbose_name_plural': 'Images Types',
            },
        ),
        migrations.CreateModel(
            name='ImageTypeCategoryRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('max_count', models.IntegerField(default=1, help_text='Maximum number of images by this image type in category', verbose_name='Count')),
                ('category', models.ForeignKey(verbose_name='Category', to='shop.Category')),
                ('image_type', models.ForeignKey(verbose_name='Image type', to='shop.ImageType')),
            ],
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Manufacturer')),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('logo', models.ImageField(upload_to=b'H:/GITHUB/virtenviro\\..\\media\\img\\shop\\manufacturers', null=True, verbose_name='Logo', blank=True)),
                ('country', models.CharField(max_length=150, null=True, verbose_name='Country', blank=True)),
                ('city', models.CharField(max_length=150, null=True, verbose_name='City', blank=True)),
                ('address', models.CharField(max_length=255, null=True, verbose_name='Address', blank=True)),
                ('phones', models.TextField(null=True, verbose_name='Phones', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Manufacturer',
                'verbose_name_plural': 'Manufacturers',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', models.CharField(max_length=60, null=True, verbose_name='Slug', blank=True)),
                ('articul', models.CharField(max_length=200, null=True, verbose_name='Articul', blank=True)),
                ('unique_code', models.CharField(unique=True, max_length=250, verbose_name='Unique code')),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('price', models.FloatField(default=0.0, verbose_name='Price')),
                ('meta_title', models.CharField(max_length=250, null=True, verbose_name='Meta Title', blank=True)),
                ('meta_keywords', models.TextField(null=True, verbose_name='Meta Keywords', blank=True)),
                ('meta_description', models.TextField(null=True, verbose_name='Meta Description', blank=True)),
                ('ordering', models.IntegerField(default=0, null=True, verbose_name='Ordering', blank=True)),
                ('view_count', models.IntegerField(default=0, null=True, verbose_name='Count of views', blank=True)),
                ('category', models.ForeignKey(related_name='children', verbose_name='Category', blank=True, to='shop.Category', null=True)),
                ('manufacturer', models.ForeignKey(verbose_name='Manufacturer', blank=True, to='shop.Manufacturer', null=True)),
                ('subcategory', models.ManyToManyField(related_name='products', verbose_name='Subcategory', to='shop.Category', blank=True)),
            ],
            options={
                'ordering': ['ordering', 'name'],
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.TextField(verbose_name='Value')),
                ('product', models.ForeignKey(verbose_name='Product', to='shop.Product')),
            ],
            options={
                'ordering': ['property_type__name', 'value'],
                'verbose_name': 'Property',
                'verbose_name_plural': 'Properties',
            },
        ),
        migrations.CreateModel(
            name='PropertyType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('data_type', models.IntegerField(default=-1, verbose_name='Data type', choices=[(-1, 'Integer'), (-2, 'Float'), (-3, 'String'), (-4, 'Text'), (-5, 'Boolean'), (-6, 'Html')])),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Properties type',
                'verbose_name_plural': 'Properties Types',
            },
        ),
        migrations.CreateModel(
            name='PropertyTypeCategoryRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('max_count', models.IntegerField(default=1, help_text='Maximum number of properties by this property type in category', verbose_name='Count')),
                ('category', models.ForeignKey(verbose_name='Category', to='shop.Category')),
                ('property_type', models.ForeignKey(verbose_name='Property Type', to='shop.PropertyType')),
            ],
        ),
        migrations.AddField(
            model_name='propertytype',
            name='category',
            field=models.ManyToManyField(to='shop.Category', through='shop.PropertyTypeCategoryRelation'),
        ),
        migrations.AddField(
            model_name='property',
            name='property_type',
            field=models.ForeignKey(to='shop.PropertyType'),
        ),
        migrations.AddField(
            model_name='imagetype',
            name='category',
            field=models.ManyToManyField(to='shop.Category', verbose_name='Production Type', through='shop.ImageTypeCategoryRelation'),
        ),
        migrations.AddField(
            model_name='image',
            name='image_type',
            field=models.ForeignKey(verbose_name='Image Type', to='shop.ImageType'),
        ),
        migrations.AddField(
            model_name='image',
            name='product',
            field=models.ForeignKey(verbose_name='Product', to='shop.Product'),
        ),
        migrations.AddField(
            model_name='file',
            name='product',
            field=models.ForeignKey(verbose_name='Product', to='shop.Product'),
        ),
    ]
