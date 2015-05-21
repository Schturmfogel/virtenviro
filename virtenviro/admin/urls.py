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
        'virtenviro.content.admin_views',
        url(r'^content/', include('virtenviro.content.admin_urls')),
    )