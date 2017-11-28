# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging

from django.shortcuts import render
from django.http import JsonResponse, Http404

from keyword_test import compute_scores

from .models import CitationObject


logger = logging.getLogger('django.SIKE.recsys.views')


def index(request):
    return render(request, 'rec/recsys.html', {})


def recommendations(request):
    if request.method != "GET":
        raise Http404("Only GET allowed")

    if "doi" not in request.GET:
        raise Http404("No doi GET parameter")

    if request.GET['doi'] == "blank":
        # This is really stupid but datatables is never *quite* right
        return JsonResponse({'cited_paper_url': []})

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

    score_data = {}
    for s in scores:
        score_data[s[0]] = s[1]

    for doi, paper in cite_data['cited_paper_url'].iteritems():
        if doi in score_data:
            paper['score'] = score_data[doi]
        else:
            paper['score'] = None

    return JsonResponse(cite_data)
