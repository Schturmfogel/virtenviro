# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_auto_20150515_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='slug',
            field=models.CharField(unique=True, max_length=250, verbose_name='Slug', blank=True),
        ),
    ]
