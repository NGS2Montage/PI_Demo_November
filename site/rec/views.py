# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


def index(request):
    return render(request, 'rec/recsys.html', {})


def recommendations(request):
    return JsonResponse({"status": "Implement me"})
