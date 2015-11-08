# ~*~ coding: utf-8 ~*~
__author__ = 'Kamo Petrosyan'
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.utils.http import urlquote
from django.conf import settings
from virtenviro.content.models import *
from virtenviro.content.admin_forms import *
from virtenviro.utils import paginate

template_str = 'virtenviro/admin/content/{}'
appname = 'content'


@staff_member_required
def content_page(request):
    template = template_str.format('change_list.html')

    context = {
        'appname': appname,
        'pages': paginate(Page.objects.all(), request.GET.get('page', 1), 100),
    }

    return render(request, template, context)


@staff_member_required
def content_page_edit(request, page_id):
    template = template_str.format('page_form.html')
    context = {'appname': appname}

    try:
        page = Page.objects.get(pk=page_id)
        context['current_page'] = page
    except Page.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        page_form = PagesAdminForm(request.POST)
        content_formset = ContentAdminFormset(request.POST)
    else:
        page_form = PagesAdminForm(instance=page)
        initials = []
        for lang in settings.LANGUAGES:
            initials.append({'language': lang[0]})
        content_formset = ContentAdminFormset(instance=page, initial=initials)
        content_formset.extra = 0

    context['page'] = page
    context['pages'] = paginate(Page.objects.all(), request.GET.get('page', 1), 100)
    context['page_form'] = page_form
    context['content_formset'] = content_formset

    return render(request, template, context)