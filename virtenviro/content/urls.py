from django.conf.urls import *

urlpatterns = patterns('',
    url(r'^$', 'content.views.home', name='home'),
    url(r'^[a-z0-9-_/]+$', 'content.views.view', name='page'),
)