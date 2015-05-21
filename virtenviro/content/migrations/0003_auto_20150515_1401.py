# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_page_is_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='author',
            field=models.ForeignKey(related_name='created_pages', verbose_name='Author', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
