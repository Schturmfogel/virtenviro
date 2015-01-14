#~*~ coding: utf-8 ~*~
from django.shortcuts import render
from django.http import Http404


def home(request):
    render(
        request,
        'admin/home.html',
        {}
    )