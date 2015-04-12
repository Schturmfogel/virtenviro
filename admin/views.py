#~*~ coding: utf-8 ~*~
from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return render(
        request,
        'admin/home.html',
        {}
    )