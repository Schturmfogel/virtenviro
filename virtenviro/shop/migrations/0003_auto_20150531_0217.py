# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0002_seller_map_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name='Name')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Order status',
                'verbose_name_plural': 'Order statuses',
            },
        ),
        migrations.CreateModel(
            name='ProductOrderRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField(default=1, verbose_name='Count')),
                ('order', models.ForeignKey(verbose_name='Order', to='shop.Order')),
                ('product', models.ForeignKey(verbose_name='Product', to='shop.Product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ManyToManyField(to='shop.Product', verbose_name='Product', through='shop.ProductOrderRelation'),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.ForeignKey(verbose_name='Status', to='shop.OrderStatus'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL),
        ),
    ]
