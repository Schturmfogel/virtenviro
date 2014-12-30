from django.conf.urls import patterns, include, url
from django.contrib import admin
from filebrowser.sites import site
from django.conf import settings


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'samplesite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    url(r'^$', 'virtenviro.content.views.home', name='home'),
    url(r'^[0-9A-Za-z-_.//]+$', 'virtenviro.content.views.view', name='page'),
)
