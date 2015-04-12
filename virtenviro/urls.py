#~*~ coding: utf-8 ~*~
import os
from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'virtenviro.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include('admin.urls')),
                       url(r'^accounts/', include('registration.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                                {'document_root': settings.STATIC_ROOT}),
                            url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                                {'document_root': settings.MEDIA_ROOT}),)
