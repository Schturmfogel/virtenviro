# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_remove_product_unique_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='propertytypecategoryrelation',
            name='slug',
            field=models.CharField(max_length=60, null=True, verbose_name='Slug', blank=True),
        ),
    ]
