# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse, Http404

from main import fetch_data_helper


def index(request):
    return render(request, 'rec/recsys.html', {})


def recommendations(request):
    if request.method != "GET":
        raise Http404("Only GET allowed")

    if "doi" not in request.GET:
        raise Http404("No doi GET parameter")

    return JsonResponse(fetch_data_helper(request.GET['doi']))
