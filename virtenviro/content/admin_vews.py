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


@staff_member_required
def content_page(request):
    template = template_str.format('change_list.html')

    context = {
        'pages': Page.objects.filter(parent__isnull=True),
    }

    return render(request, template, context)


@staff_member_required
def content_page_edit(request, page_id):
    template = template_str.format('page_form.html')
    context = {}

    try:
        page = Page.objects.get(pk=page_id)
        context['current_page'] = page
    except Page.DoesNotExist:
        raise Http404

    initials = []
    for lang in settings.LANGUAGES:
        if page.get_content(language=lang) is None:
            initials.append({'language': lang[0], 'author': request.user})

    if request.method == 'POST':
        page_form = PagesAdminForm(request.POST, instance=page)
        content_formset = ContentAdminFormset(request.POST, request.FILES, instance=page, initial=initials)
        if page_form.is_valid() and content_formset.is_valid():
            page = page_form.save()
            content_formset.save()
    else:
        page_form = PagesAdminForm(instance=page)
        content_formset = ContentAdminFormset(instance=page, initial=initials)

    content_formset.extra = len(initials)

    context['page'] = page
    context['pages'] = paginate(Page.objects.all(), request.GET.get('page', 1), 100)
    context['page_form'] = page_form
    context['content_formset'] = content_formset

    return render(request, template, context)

