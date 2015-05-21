# ~*~ coding: utf-8 ~*~
__author__ = 'Kamo Petrosyan'
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.http import urlquote
from django.conf import settings
from virtenviro.content.models import *

template_str = 'virtenviro/admin/content/%s'

@login_required
def home(request):
    return render(request, template_str % 'home.html', {})