# ~*~ coding: utf-8 ~*~
__author__ = 'Kamo Petrosyan'
from django.conf.urls import *
from django.conf import settings
from views import *


urlpatterns = patterns('virtenviro.views',
    url(r'^$', index, name='home'),
)
if 'virtenviro.content' in settings.INSTALLED_APPS:
    urlpatterns += patterns(
        'virtenviro.admin.views',
        url(r'^content/$', 'content_page', name='content'),
        url(r'^content/(?P<action>\w+)/$', 'content_page', name='content_page_add'),
        url(r'^content/(?P<action>\w+)/(?P<page_id>\d+)/$', 'content_page', name='content_page_action'),
    )

if 'virtenviro.shop' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^shop/$', 'virtenviro.admin.views.shop', name='vadmin_shop'),
        url(r'^shop/import_yml/$', 'virtenviro.shop.views.import_yml', name='vadmin_import_yml'),
    )