from django.conf.urls import *
from django.conf import settings
from views import *


urlpatterns = patterns('virtenviro.views',
    url(r'^$', index, name='home'),
)