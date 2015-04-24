# ~*~ coding: utf-8 ~*~
__author__ = 'Kamo Petrosyan'
from django.shortcuts import render, redirect
from django.http import Http404
from django.utils.http import urlquote
from django.conf import settings
from virtenviro.content.models import *

template_str = 'admin/virtenviro/%s'


def index(request):
    base_pages = Page.objects.filter(parent__isnull=True)
    context = {'base_pages': base_pages,}
    return render(request, template_str % 'index.html', context)