import logging

from huey.contrib.djhuey import db_task, enqueue

from .models import Paper


logger = logging.getLogger('recsys.tasks')


@db_task()
def fetch_doi(doi):
    return Paper.create_from_doi(doi)


@db_task()
def fetch(paper):
    logger.debug("Fetching {}".format(paper))
    paper.fetch()
    return paper


def do_work():
    # p = Paper.objects.filter(fetched=False).order_by('added_to_db').first()

    wrapper = None
    for p in Paper.objects.filter(fetched=False):
        print("Going to enqueue {}".format(p))
        logger.debug("Going to enqueue work on {}".format(p))
        wrapper = fetch(p)

    if wrapper:
        wrapper.get(blocking=True)
        print("Done with round")
        logger.debug("Done with a round")
