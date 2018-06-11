import huey
from huey.contrib.djhuey import db_task, enqueue

from .models import Paper


@db_task()
def fetch_doi(doi):
    return Paper.create_from_doi(doi)


@db_task()
def follow_something():
    p = Paper.objects.filter(fetched=False).order_by('-added_to_db').first()
    return p.fetch()


@db_task()
def follow(paper):
    paper.fetch()
    return paper


@db_task()
def download_pdf(paper):
    paper.download_pdf()
    return paper


@db_task()
def fetch_cocitations(paper):
    print("Implement fetch_cocitations")
    return paper


def do_work():
    p = Paper.objects.filter(fetched=False).order_by('added_to_db').first()

    if not p.citation_only:
        pipe = (follow.s(p)
                .then(fetch_cocitations)
                .then(download_pdf))
        results = enqueue(pipe)

        print([result.get(True) for result in results])
    else:
        follow(p)
