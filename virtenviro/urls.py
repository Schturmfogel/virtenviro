import os
from django.conf import settings
from django.conf.urls import *
from django.contrib import admin
from filebrowser.sites import site

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'content.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^admin/', include(admin.site.urls)),
)