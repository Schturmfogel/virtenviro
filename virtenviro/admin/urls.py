# ~*~ coding: utf-8 ~*~
__author__ = 'Kamo Petrosyan'
from django.conf.urls import url, include
from django.conf import settings

app_name='vadmin'

urlpatterns = [
    url(r'^$', 'virtenviro.admin.views.index', name='home'),
]

if 'virtenviro.content' in settings.INSTALLED_APPS:
    urlpatterns += [
        url(r'^content/$', 'virtenviro.content.admin_vews.content_page', name='content'),
        url(r'^content/(?P<page_id>\d+)/$', 'virtenviro.content.admin_vews.content_page_edit', name='content_page_edit'),
        # url(r'^content/(?P<action>\w+)/(?P<page_id>\d+)/$', 'content_page', name='content_page_action'),
    ]

if 'virtenviro.shop' in settings.INSTALLED_APPS:
    urlpatterns += [
        url(r'^shop/$', 'virtenviro.admin.views.shop', name='vadmin_shop'),
        url(r'^shop/import_yml/$', 'virtenviro.shop.views.import_yml', name='vadmin_import_yml'),
    ]
