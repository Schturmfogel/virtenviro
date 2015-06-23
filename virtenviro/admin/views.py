# ~*~ coding: utf-8 ~*~
__author__ = 'Kamo Petrosyan'
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.http import urlquote
from django.conf import settings
from virtenviro.content.models import *
from virtenviro.utils import paginate

template_str = 'virtenviro/admin/%s'


@login_required
def index(request):
    base_pages = Page.objects.filter(parent__isnull=True)
    context = {
        'base_pages': base_pages,
    }
    return render(request, template_str % 'index.html', context)


@login_required
def content_page(request, action=None, page_id=None):
    template = 'virtenviro/admin/content/change_list.html'
    context = {
        'appname': 'content',
    }
    if action is None:
        context['pages'] = paginate(Page.objects.all(), request.GET.get('page', 1), 100)
    elif page_id is None and action == 'add':
        pass
    else:
        if page_id is None:
            raise Http404
        else:
            if action == 'delete':
                pass
            elif action == 'edit':
                pass
            else:
                raise Http404
    return render(request, template, context)


@login_required
def shop(request):

    template = 'virtenviro/admin/shop/home.html'
    context = {
        'appname': 'shop',
    }
    return render(request, template, context)