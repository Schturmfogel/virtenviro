# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_product_unique_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='unique_code',
            field=models.CharField(unique=True, max_length=250, verbose_name='Unique code', blank=True),
        ),
    ]
