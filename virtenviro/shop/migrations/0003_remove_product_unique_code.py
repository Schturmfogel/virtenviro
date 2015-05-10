# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_product_unique_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='unique_code',
        ),
    ]
