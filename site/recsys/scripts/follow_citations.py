import logging

from recsys.forms import add_paper
from recsys.models import Paper, Citation
from .scraper import Record, MissingDataException


logger = logging.getLogger('recsys.scripts.follow_citations')


def run(doi=None):
    objects = Citation.objects.filter(record_id=None) if doi is None else Paper.objects.get(doi=doi).citation_set

    # for each citation
    # If we don't already have this citation (Papers need CID?)
    #    fetch it
    #    link citation's Paper object to this Citation
    # If we do, link them

    for c in objects.filter(citation_only=False):
        try:
            r = Record(c.cid, "cid")

            qs = Paper.objects.filter(doi=r.doi)
            if qs.exists():
                c.paper = qs[0]
                logger.debug("Citation already fetched: {} cites {}".format(doi, c.cid))
            else:
                output = add_paper(r.toJSON())
                logger.debug("Saving {} to record for {}".format(output[2], c))
                c.record = output[2]  # link citation object to paper object
                c.save()
                logger.debug("Citation followed: {} cites {} {}".format(doi, c.cid, output))
        except MissingDataException:
            logger.error("Skipping {}".format(c.cid))
