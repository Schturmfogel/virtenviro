# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_propertytypecategoryrelation_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertySlug',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.TextField(verbose_name='Value')),
                ('slug', models.CharField(max_length=60, verbose_name='Slug')),
                ('property_type', models.ForeignKey(to='shop.PropertyType')),
            ],
            options={
                'ordering': ['value'],
                'verbose_name': 'Property slug',
                'verbose_name_plural': 'Property slugs',
            },
        ),
    ]
