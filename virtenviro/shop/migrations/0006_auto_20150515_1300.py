# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_propertyslug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertyslug',
            name='property_type',
            field=models.ForeignKey(verbose_name='Propert type', to='shop.PropertyType'),
        ),
    ]
