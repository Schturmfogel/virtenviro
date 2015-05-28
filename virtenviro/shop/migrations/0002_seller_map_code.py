# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='map_code',
            field=models.TextField(null=True, verbose_name="Map's code", blank=True),
        ),
    ]
