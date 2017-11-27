# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.shortcuts import render
from django.http import JsonResponse, Http404

from keyword_test import compute_scores

from .models import CitationObject


def index(request):
    return render(request, 'rec/recsys.html', {})


def recommendations(request):
    if request.method != "GET":
        raise Http404("Only GET allowed")

    if "doi" not in request.GET:
        raise Http404("No doi GET parameter")

    cite_obj = CitationObject.objects.get_or_build(request.GET['doi'])
    cite_data = json.loads(cite_obj.cite_data)

    return JsonResponse(cite_data)


def scores(request):
    if request.method != "GET":
        raise Http404("Only GET allowed")

    if "doi" not in request.GET:
        raise Http404("No doi GET parameter")

    cite_obj = CitationObject.objects.get_or_build(request.GET['doi'])
    cite_data = json.loads(cite_obj.cite_data)
    scores = compute_scores(cite_data, cite_obj.doi)
    print("*******SCORES*******")
    print(scores)
    print("*******SCORES*******")

    return JsonResponse(scores)
