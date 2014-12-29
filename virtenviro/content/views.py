# ~*~ coding: utf-8 ~*~
from django.shortcuts import render, get_object_or_404
from virtenviro.content.models import *
from django.http import Http404


def home(request):
    try:
        page = Page.objects.get(is_home=True)
    except Page.DoesNotExist:
        raise Http404
    return render(request, page.template.filename, {'page': page}, )


def view(request):
    """

    :param request: request
    :return: render
    """
    try:
        path = request.path.lstrip('page')
        path = path.strip('/').split('/')
        page = Page.objects.get(slug=path[-1], is_home=False) or Page.objects.get(slug=path[-1], parent__slug=path[-2],
                                                                                  is_home=False)
    except Page.DoesNotExist:
        raise Http404
    return render(request, page.template.filename, {'page': page, 'request': request}, )


def show_as_blog(request, parent):
    """

    :param request:
    :param parent: Page object - category of the blog
    :return: render
    """
    pass


def show_as_simple_page(request, page):
    """

    :param request:
    :param parent: Page object - category of the blog
    :return: render
    """
    pass


def app(request, page, app):
    """

    :param request:
    :param page: Page
    :param app: application
    :return:
    """
    pass