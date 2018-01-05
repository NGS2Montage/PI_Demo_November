import logging

from recsys.forms import add_paper
from .scraper import Record, MissingDataException


logger = logging.getLogger('recsys.scripts.collect_paper')


def run(doi):
    try:
        r = Record(doi)
        output = add_paper(r.toJSON())
        logger.debug("Paper collected: {} {}".format(doi, output[:2]))
    except MissingDataException:
        logger.error("MissingDataException for {}")
