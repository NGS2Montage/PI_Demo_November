import json
import logging

from django.db import models

from main import fetch_data
from keyword_test import compute_scores


logger = logging.getLogger('django.SIKE.recsys.views')


class BuilderManager(models.Manager):
    def get_or_build(self, doi, *args, **kwargs):
        r = self.filter(doi=doi, *args, **kwargs)
        if r.exists():
            return r[0]

        logger.debug("Fetching data for {}".format(doi))
        cite_data = fetch_data(doi)
        logger.debug("Computing scores for {}".format(doi))
        scores = compute_scores(cite_data, doi)

        scored_papers = {}
        for score_pair in scores:
            s_doi = score_pair[0]
            score = score_pair[1]
            if s_doi in cite_data['cited_paper_url']:
                scored_papers[s_doi] = cite_data['cited_paper_url'][s_doi]
                scored_papers[s_doi]['score'] = score

        cite_data['cited_paper_url'] = scored_papers

        return self.create(doi=doi, cite_data=json.dumps(cite_data))
